from google.cloud import firestore
from classes.gemini_model_pricing import GeminiModelPricing
from classes.user import User
from classes.model_token_budget import ModelTokenBudget
from db.collections import users_collection, model_token_budgets_collection
from constants.gemini_models import (
    GEMINI_3_1_PRO_PREVIEW,
    GEMINI_3_1_FLASH_LITE_PREVIEW,
    GEMINI_3_FLASH_PREVIEW,
    GEMINI_2_5_FLASH,
    GEMINI_2_5_FLASH_LITE
)

class UserRequestManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRequestManager, cls).__new__(cls)
            cls._instance.token_ratios = {
                GEMINI_3_1_PRO_PREVIEW: 3.8,
                GEMINI_3_1_FLASH_LITE_PREVIEW: 4.0,
                GEMINI_3_FLASH_PREVIEW: 4.0,
                GEMINI_2_5_FLASH: 4.0,
                GEMINI_2_5_FLASH_LITE: 4.2,
            }
            # Initialize budgets if they don't exist in Firestore
            cls._instance.init_model_token_budgets()
        return cls._instance

    def increment_user_request(self, email: str):
        docs = users_collection.where("email", "==", email).stream()
        doc_found = False
        current_count = 0
        
        for doc in docs:
            doc_found = True
            current_count = doc.to_dict().get("request_count", 0)
            doc.reference.update({"request_count": firestore.Increment(1)})
            break
            
        if not doc_found:
            new_user = User(email=email, request_count=1)
            users_collection.add(new_user.to_dict())
            current_count = 0
            
        new_count = current_count + 1
        print(f"[USER_REQUEST_MANAGER] increment_user_request: email={email}, count={new_count}", flush=True)
        return new_count
    
    def get_user_request_count(self, email: str):
        docs = users_collection.where("email", "==", email).stream()
        for doc in docs:
            return doc.to_dict().get("request_count", 0)
        return 0

    def init_model_token_budgets(self):
        gemini_pricing_model = GeminiModelPricing()
        for model_name, model_data in gemini_pricing_model.models.items():
            input_budget = model_data["daily_project_input_token_budget"]
            output_budget = model_data["daily_project_output_token_budget"]
            
            docs = model_token_budgets_collection.where("model_name", "==", model_name).stream()
            doc_found = False
            for doc in docs:
                doc_found = True
                break
            
            if not doc_found:
                new_budget = ModelTokenBudget(
                    model_name=model_name,
                    remaining_input_tokens=input_budget,
                    remaining_output_tokens=output_budget
                )
                model_token_budgets_collection.add(new_budget.to_dict())
        
    def update_model_token_budget(self, model_name, input_tokens = 0, output_tokens = 0):
        docs = model_token_budgets_collection.where("model_name", "==", model_name).stream()
        doc_found = False
        for doc in docs:
            doc_found = True
            doc.reference.update({
                "remaining_input_tokens": firestore.Increment(-input_tokens),
                "remaining_output_tokens": firestore.Increment(-output_tokens)
            })
            break
            
        if not doc_found:
            self.init_model_token_budgets()
            self.update_model_token_budget(model_name, input_tokens, output_tokens)

    def get_model_remaining_tokens(self, model_name):
        docs = model_token_budgets_collection.where("model_name", "==", model_name).stream()
        for doc in docs:
            data = doc.to_dict()
            return {
                "remaining_input_tokens": data.get("remaining_input_tokens", 0),
                "remaining_output_tokens": data.get("remaining_output_tokens", 0)
            }
            
        self.init_model_token_budgets()
        # Retry after init
        docs = model_token_budgets_collection.where("model_name", "==", model_name).stream()
        for doc in docs:
            data = doc.to_dict()
            return {
                "remaining_input_tokens": data.get("remaining_input_tokens", 0),
                "remaining_output_tokens": data.get("remaining_output_tokens", 0)
            }
            
        return None

    def estimate_input_tokens(self, text: str, model_name: str) -> int:
        # Estimate the number of input tokens for a given string and model.
        # Uses a conservative character-to-token ratio.
        ratio = self.token_ratios.get(model_name, 4.0)
        return int(len(text) / ratio) + 1


user_request_manager = UserRequestManager()

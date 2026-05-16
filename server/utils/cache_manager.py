import datetime
import pytz
from cachetools import TTLCache
from classes.gemini_model_pricing import GeminiModelPricing
from constants.gemini_models import (
    GEMINI_3_1_PRO_PREVIEW,
    GEMINI_3_1_FLASH_LITE_PREVIEW,
    GEMINI_3_FLASH_PREVIEW,
    GEMINI_2_5_PRO,
    GEMINI_2_5_FLASH,
    GEMINI_2_5_FLASH_LITE
)

class RequestCacheManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestCacheManager, cls).__new__(cls)
            # maxsize to 10000 users, ttl to 24 hours (86400 seconds)
            cls._instance.cache = TTLCache(maxsize=10000, ttl=86400)
            cls._instance.current_day = cls._instance._get_current_pt_day()
            
            cls._instance.token_ratios = {
                GEMINI_3_1_PRO_PREVIEW: 3.8,
                GEMINI_3_1_FLASH_LITE_PREVIEW: 4.0,
                GEMINI_3_FLASH_PREVIEW: 4.0,
                GEMINI_2_5_PRO: 3.8,
                GEMINI_2_5_FLASH: 4.0,
                GEMINI_2_5_FLASH_LITE: 4.2,
            }
            cls._instance.init_model_token_budgets()
        return cls._instance

    def _get_current_pt_day(self):
        # GCP quota resets at midnight Pacific Time
        pt_tz = pytz.timezone("America/Los_Angeles")
        return datetime.datetime.now(pt_tz).date()

    def _check_and_reset_cache(self):
        current_day = self._get_current_pt_day()
        if current_day != self.current_day:
            self.cache.clear()
            self.current_day = current_day
            self.init_model_token_budgets()

    def increment_user_request(self, email: str):
        self._check_and_reset_cache()
        if email in self.cache:
            self.cache[email] += 1
        else:
            self.cache[email] = 1
        return self.cache[email]
    
    def get_user_request_count(self, email: str):
        self._check_and_reset_cache()
        return self.cache.get(email, 0)

    
    def init_model_token_budgets(self):
        gemini_pricing_model = GeminiModelPricing()
        for model_name, model_data in gemini_pricing_model.models.items():
            self.cache[model_name] = { 
                "remaining_input_tokens": model_data["daily_project_input_token_budget"], 
                "remaining_output_tokens": model_data["daily_project_output_token_budget"]
            }
        
    def update_model_token_budget(self, model_name, input_tokens = 0, output_tokens = 0):
        self._check_and_reset_cache()
        if model_name not in self.cache:
            self.init_model_token_budgets()
            
        if model_name in self.cache:
            self.cache[model_name]["remaining_input_tokens"] = max(0, self.cache[model_name]["remaining_input_tokens"] - input_tokens)
            self.cache[model_name]["remaining_output_tokens"] = max(0, self.cache[model_name]["remaining_output_tokens"] - output_tokens)

    def get_model_remaining_tokens(self, model_name):
        self._check_and_reset_cache()
        if model_name not in self.cache:
            self.init_model_token_budgets()
            
        if model_name in self.cache:
            return {
                "remaining_input_tokens": self.cache[model_name]["remaining_input_tokens"],
                "remaining_output_tokens": self.cache[model_name]["remaining_output_tokens"]
            }
        return None

        
    def estimate_input_tokens(self, text: str, model_name: str) -> int:
        """
        Estimate the number of input tokens for a given string and model.
        Uses a conservative character-to-token ratio.
        """
        ratio = self.token_ratios.get(model_name, 4.0)
        return int(len(text) / ratio) + 1


request_cache = RequestCacheManager()

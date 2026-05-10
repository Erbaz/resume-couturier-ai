import os
from dotenv import load_dotenv
from constants.gemini_models import (
    GEMINI_3_1_PRO_PREVIEW,
    GEMINI_3_1_FLASH_LITE_PREVIEW,
    GEMINI_3_FLASH_PREVIEW,
    GEMINI_2_5_PRO,
    GEMINI_2_5_FLASH,
    GEMINI_2_5_FLASH_LITE
)

load_dotenv()
"""
Gemini API Text-Only Model Pricing
Gemini 2.5+ models in Standard tier (Paid Tier)
 
All prices: USD per 1M tokens
Daily budgets: Token counts equivalent to DAILY_BUDGET_USD for input and output separately
Last updated: April 2026
"""
 
# Global constant: Daily budget per token type (input/output) per model
DAILY_BUDGET_USD = float(os.getenv("GEMINI_DAILY_BUDGET_USD", 0.05))
 
 
class GeminiModelPricing:
    """
    Manages Gemini model pricing and token budgets.
    Read-only access to pricing data.
    
    Attributes:
        models: Dictionary of model configurations with pricing and budget info
    """
    
    def __init__(self):
        """Initialize with all text-only Gemini 2.5+ models and their pricing."""
        self.models = {
            GEMINI_3_1_PRO_PREVIEW: {
                "input_tokens_per_1M_usd": 2.00,
                "output_tokens_per_1M_usd": 12.00,
            },
            GEMINI_3_1_FLASH_LITE_PREVIEW: {
                "input_tokens_per_1M_usd": 0.25,
                "output_tokens_per_1M_usd": 1.50,
            },
            GEMINI_3_FLASH_PREVIEW: {
                "input_tokens_per_1M_usd": 0.50,
                "output_tokens_per_1M_usd": 3.00,
            },
            GEMINI_2_5_PRO: {
                "input_tokens_per_1M_usd": 1.25,
                "output_tokens_per_1M_usd": 10.00,
            },
            GEMINI_2_5_FLASH: {
                "input_tokens_per_1M_usd": 0.30,
                "output_tokens_per_1M_usd": 2.50,
            },
            GEMINI_2_5_FLASH_LITE: {
                "input_tokens_per_1M_usd": 0.10,
                "output_tokens_per_1M_usd": 0.40,
            },
        }
        
        # Calculate budgets from pricing
        self._calculate_all_budgets()
 
    def _calculate_all_budgets(self) -> None:
        """
        Calculate token budgets for all models based on DAILY_BUDGET_USD.
        """
        for model_name, model_data in self.models.items():
            model_data["daily_project_input_token_budget"] = int(
                (DAILY_BUDGET_USD / model_data["input_tokens_per_1M_usd"]) * 1_000_000
            )
            model_data["daily_project_output_token_budget"] = int(
                (DAILY_BUDGET_USD / model_data["output_tokens_per_1M_usd"]) * 1_000_000
            )
 
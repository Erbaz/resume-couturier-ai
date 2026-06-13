import os
from fastapi import APIRouter, Depends
from middleware.authMiddleware import verify_google_oauth_token
from utils.cache_manager import user_request_manager
from utils.global_request_manager import global_request_manager

router = APIRouter()

@router.get("/")
async def get_budget(token_data: dict = Depends(verify_google_oauth_token)):
    user_email = token_data.get("email")
    
    # User Request Limit
    try:
        user_limit = int(os.getenv("RATE_LIMIT_PER_USER", "50"))
    except ValueError:
        user_limit = 50
    
    user_requests = user_request_manager.get_user_request_count(user_email)
    user_requests_left = max(0, user_limit - user_requests)
    
    # Model Token Budgets
    models_budget = user_request_manager.get_all_model_budgets()
    
    # Global Request Budget
    gemini_budget_utilized, global_requests = global_request_manager.get_current_state()
    
    try:
        daily_budget_limit = float(os.getenv("DAILY_GEMINI_BUDGET", "0.5"))
    except ValueError:
        daily_budget_limit = 0.5
        
    try:
        daily_req_limit = int(os.getenv("DAILY_TOTAL_REQUESTS", "5000"))
    except ValueError:
        daily_req_limit = 5000
        
    budget_percent_left = 100.0 * max(0.0, (daily_budget_limit - gemini_budget_utilized) / daily_budget_limit)
    requests_percent_left = 100.0 * max(0.0, (daily_req_limit - global_requests) / daily_req_limit)
    
    global_request_budget_left_percent = min(budget_percent_left, requests_percent_left)
    
    return {
        "user_requests_left": user_requests_left,
        "models": models_budget,
        "global_request_budget_left_percent": global_request_budget_left_percent
    }

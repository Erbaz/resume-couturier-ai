from fastapi import Depends
from middleware.authMiddleware import verify_google_oauth_token
from utils.cache_manager import request_cache

def rate_limit_middleware(token_info: dict = Depends(verify_google_oauth_token)):
    """
    Middleware that runs after verify_google_oauth_token.
    Updates the request count in the cache for the given user email.
    """
    email = token_info.get("email")
    if email:
        request_cache.increment_user_request(email)
    
    # Future logic for blocking if limit is exceeded can be added here
    
    return token_info

import os
from fastapi import Depends, HTTPException, status, Response
from middleware.authMiddleware import verify_google_oauth_token
from utils.cache_manager import request_cache

def rate_limit_middleware(body: dict, response: Response, token_info: dict = Depends(verify_google_oauth_token)):
    """
    Middleware that runs after verify_google_oauth_token.
    Updates the request count in the cache for the given user email.
    Blocks the request if the daily limit is exceeded.
    """
    email = token_info.get("email")
    if email:
        # Increment and get the current count
        count = request_cache.increment_user_request(email)
        
        # Get the limit from environment variables
        limit_str = os.getenv("RATE_LIMIT_PER_USER")
        try:
            limit = int(limit_str) if limit_str else 50  # Default to 50 if not set
        except ValueError:
            limit = 50

        # If the threshold is reached, add the flag to headers
        if count >= limit:
            response.headers["x-rate-limit-flag"] = "true"

        # If the threshold is exceeded, block the request
        if count > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Daily request limit reached. Please try again tomorrow.",
                headers={"x-rate-limit-flag": "true"}
            )        
            

    
    return token_info

from datetime import timedelta
from server.utils import get_la_start_of_day
import os
from fastapi import Depends, HTTPException, status, Response
from middleware.authMiddleware import verify_google_oauth_token
from utils.cache_manager import user_request_manager

def rate_limit_middleware(response: Response, token_info: dict = Depends(verify_google_oauth_token)):
    """
    Middleware that runs after verify_google_oauth_token.
    Updates the request count in the cache for the given user email.
    Blocks the request if the daily limit is exceeded.
    """
    email = token_info.get("email")
    print(f"[RATE_LIMIT_MIDDLEWARE] Invoked for email={email}", flush=True)
    if email:
        # Increment and get the current count
        count = user_request_manager.increment_user_request(email)
        
        # Get the limit from environment variables
        limit_str = os.getenv("RATE_LIMIT_PER_USER")
        try:
            limit = int(limit_str) if limit_str else 50  # Default to 50 if not set
        except ValueError:
            limit = 50
        print(f"[RATE_LIMIT_MIDDLEWARE] email={email}, count={count}, limit={limit}", flush=True)

        # If the threshold is reached, add the flag to headers
        if count >= limit:
            response.headers["x-rate-limit-flag"] = "true"

        # If the threshold is exceeded, block the request
        next_day = (get_la_start_of_day() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S %Z")
        
        if count > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Daily request limit reached. Please try again after {next_day}",
                headers={"x-rate-limit-flag": "true", "x-rate-limit-retry-after": next_day}
            )        
            

    
    return token_info

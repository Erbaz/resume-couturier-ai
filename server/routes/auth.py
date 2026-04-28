from fastapi import APIRouter, Depends
from middleware.rateLimitMiddleware import rate_limit_middleware

router = APIRouter()

@router.post("/auth")
async def auth(token_data: dict = Depends(rate_limit_middleware)):
    """
    Endpoint protected by OAuth. 
    It requires a valid Google access token in the Authorization header.
    """
    # token_data contains the validated Google user info (e.g., sub/email/aud)
    user_id = token_data.get("sub")
    email = token_data.get("email")
    
    return {
        "message": "Authentication successful",
        "user_email": email,
        "token_details": token_data
    }

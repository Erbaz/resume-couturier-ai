from fastapi import APIRouter, Depends
from middleware.authMiddleware import verify_google_oauth_token

router = APIRouter()

@router.post("/auth")
async def auth(token_data: dict = Depends(verify_google_oauth_token)):
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

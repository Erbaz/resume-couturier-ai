from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

def verify_google_oauth_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    FastAPI Dependency to validate Google OAuth access token.
    Expects 'Authorization: Bearer <token>' in headers.
    """
    token = credentials.credentials
    
    # Use Google's tokeninfo endpoint to validate the access token
    # For ID tokens (JWTs), you would use the google-auth package: 
    # google.oauth2.id_token.verify_oauth2_token
    tokeninfo_url = f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
    response = requests.get(tokeninfo_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    token_info = response.json()
    
    expected_client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    
    if token_info.get("aud") != expected_client_id:
        raise HTTPException(status_code=401, detail="Token was not issued for this application.")

    return token_info
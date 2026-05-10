import google.auth
import google.auth.transport.requests

def get_google_auth_token():
    """
    Fetches a Google Auth token using Application Default Credentials (ADC).
    This works on Cloud Run (using service account) and locally (using gcloud auth application-default login).
    """
    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    credentials, project = google.auth.default(scopes=scopes)
    
    # Create a request object to refresh the credentials
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    
    return credentials.token

from google.cloud import firestore
import dotenv
import os

dotenv.load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
try:
    db = firestore.Client(project=project_id)
    print(f"Successfully initialized Firestore client for project: {project_id}")
except Exception as e:
    print(f"Error initializing Firestore client: {e}")
    db = None
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, privacy, resume
from middleware.rateLimitMiddleware import rate_limit_middleware

load_dotenv()

chrome_extension_ids = [
    ext_id.strip()
    for ext_id in os.getenv("CHROME_EXTENSION_ID", "").split(",")
    if ext_id.strip()
]
if not chrome_extension_ids:
    raise RuntimeError(
        "CHROME_EXTENSION_ID must be set (comma-separated Chrome extension IDs for CORS)."
    )

app = FastAPI(title="Resume Couturier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"chrome-extension://{ext_id}" for ext_id in chrome_extension_ids],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assets_dir = os.path.join(os.path.dirname(__file__), "assets")
if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

app.include_router(auth.router, tags=["Auth"])
app.include_router(privacy.router, tags=["Privacy"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])

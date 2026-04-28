import os

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, resume
from middleware.rateLimitMiddleware import rate_limit_middleware

app = FastAPI(title="Resume Couturier API")

# Add CORS middleware to allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assets_dir = os.path.join(os.path.dirname(__file__), "assets")
if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

app.include_router(auth.router, tags=["Auth"], dependencies=[Depends(rate_limit_middleware)])
app.include_router(resume.router, prefix="/resume", tags=["Resume"], dependencies=[Depends(rate_limit_middleware)])

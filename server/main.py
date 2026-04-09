import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import auth, resume, scrape

app = FastAPI(title="Resume Couturier API")

assets_dir = os.path.join(os.path.dirname(__file__), "assets")
if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

app.include_router(auth.router, tags=["Auth"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])
app.include_router(scrape.router, tags=["Scraper"])

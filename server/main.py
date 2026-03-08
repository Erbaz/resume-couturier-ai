from fastapi import FastAPI
from routes import auth, resume

app = FastAPI(title="Resume Couturier API")

app.include_router(auth.router, tags=["Auth"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])

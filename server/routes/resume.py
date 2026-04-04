from fastapi import APIRouter, HTTPException, Response, UploadFile, File, Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from constants.latex_templates import templates
from utils.latex import latex_to_pdf
from utils.parsing import parse_to_markdown
from utils.evaluator import ats_score_evaluator
from middleware.authMiddleware import verify_google_oauth_token, security
import requests
import os
import dotenv

dotenv.load_dotenv()

class GenerateResumeRequestBody(BaseModel):
    user_info: str
    job_desc: str
    custom_instructions: str

router = APIRouter()

@router.get("/latex-templates")
async def get_latex_templates():
    
    response = []
    for template in templates:
        response.append({
            "id": template["id"],
            "name": template["name"],
            "thumbnail": template["thumbnail"]
        })
        
    return response

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    try:
        content = await file.read()
        markdown_str = parse_to_markdown(content, file.filename)
        return {"markdown": markdown_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse document: {str(e)}")

@router.post("/generate/{template_id}")
async def generate_resume(template_id: str, body: GenerateResumeRequestBody, token_data: dict = Depends(verify_google_oauth_token), credentials: HTTPAuthorizationCredentials = Depends(security)):
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
        
    final_prompt = f"""
    Use the given information to construct a finalized latex code. You must not say anything else. Just respond with the latex code.
    You must not change stylistics in the template. Just try to make sure that the content is updated, and the sections and breakpoints are as per desired user instructions, or job description requirements. But it is best to maintain the format and section breakdown already defined in the template if not asked to modify.

    user infromation: {body.user_info}
    job description: {body.job_desc}
    template: {template['latex']}
    """
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise HTTPException(status_code=500, detail="GOOGLE_CLOUD_PROJECT_ID is not configured in .env")

    token = credentials.credentials
    print(f"token: {token}")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "Authorization": f"Bearer {token}",
        "x-goog-user-project": project_id,
        "Content-Type": "application/json"
    }
    data = {"contents": [{"parts": [{"text": final_prompt}]}]}
    
    ai_response = requests.post(url, headers=headers, json=data)
    
    if ai_response.status_code != 200:
        raise HTTPException(status_code=ai_response.status_code, detail=f"Google API Error: {ai_response.text}")
        
    result = ai_response.json()
    print(f"result: {result}")
    try:
        generated_latex = result["candidates"][0]["content"]["parts"][0]["text"]
        
        # Clean up Markdown formatting if provided by Gemini
        generated_latex = generated_latex.strip()
        if generated_latex.startswith("```latex"):
            generated_latex = generated_latex[8:]
        elif generated_latex.startswith("```"):
            generated_latex = generated_latex[3:]
        if generated_latex.endswith("```"):
            generated_latex = generated_latex[:-3]
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Unexpected response format from Google API")
    
    print(f"generated_latex: {generated_latex}")

    pdf_bytes = latex_to_pdf(generated_latex)
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
    score = ats_score_evaluator(pdf_bytes, body.job_desc)
    headers = {}
    if score:
        headers["X-ATS-Score-Found"] = "true"
        print(f"ATS Score Evaluation:\n{score}")
        
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)

@router.post("/score")
async def score_resume():
    return {"message": "placeholder"}

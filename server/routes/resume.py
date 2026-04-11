from fastapi import APIRouter, HTTPException, Response, UploadFile, File, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from constants.latex_templates import templates
from utils.latex import latex_to_pdf
from utils.parsing import parse_file
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
    gemini_model: str = "gemini-2.5-flash"


router = APIRouter()


@router.get("/latex-templates")
async def get_latex_templates():

    response = []
    for template in templates:
        response.append(
            {
                "id": template["id"],
                "name": template["name"],
                "thumbnail": template["thumbnail"],
            }
        )

    return response


@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...), token_data: dict = Depends(verify_google_oauth_token)
):
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400, detail="Only PDF and DOCX files are supported"
        )

    try:
        content = await file.read()
        parsed_text = parse_file(content, file.filename)
        return {"parsed_text": parsed_text}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to parse document: {str(e)}"
        )


@router.post("/generate/{template_id}")
async def generate_resume(
    template_id: str,
    body: GenerateResumeRequestBody,
    token_data: dict = Depends(verify_google_oauth_token),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    gemini_model = body.gemini_model
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    final_prompt = f"""
    Use the given information to construct a finalized latex code. You must not say anything else. Your output format will look like this:
    You must not change stylistics in the template. Just try to make sure that the content is updated, and the sections and breakpoints are as per desired user instructions, or job description requirements. But it is best to maintain the format and section breakdown already defined in the template if not asked to modify.
    You are at liberty to remove sections that are not needed, or infromation for the user is not provided or insufficient for the section.
    Your response will be validated by an ATS checker, so make sure that content is relevant, and contains keywords from the job description.
    Do make sure not to add details not already present in user information. That would be considered lying in a resume and will be rejected.
    
    user infromation: {body.user_info}
    job description: {body.job_desc}
    additional instructions: {body.custom_instructions}
    template: {template['latex']}
    """

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise HTTPException(
            status_code=500, detail="GOOGLE_CLOUD_PROJECT_ID is not configured in .env"
        )

    token = credentials.credentials
    print(f"token: {token}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent"
    headers = {
        "Authorization": f"Bearer {token}",
        "x-goog-user-project": project_id,
        "Content-Type": "application/json",
    }
    data = {"contents": [{"parts": [{"text": final_prompt}]}]}

    ai_response = requests.post(url, headers=headers, json=data)

    if ai_response.status_code != 200:
        raise HTTPException(
            status_code=ai_response.status_code,
            detail=f"Google API Error: {ai_response.text}",
        )

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
        raise HTTPException(
            status_code=500, detail="Unexpected response format from Google API"
        )

    print(f"generated_latex: {generated_latex}")

    pdf_bytes = latex_to_pdf(generated_latex)
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

    missing_keywords_prompt = f"""
    evaluate and identify the missing key words in the resume (latex code) using the job description.
    You will only respond with a list of missing keywords as a comma separated list. Say nothing else.

    resume:
    {generated_latex}

    job description:
    {body.job_desc}
    """
    missing_keywords_data = {
        "contents": [{"parts": [{"text": missing_keywords_prompt}]}]
    }
    missing_keywords_response = requests.post(
        url, headers=headers, json=missing_keywords_data
    )

    if missing_keywords_response.status_code != 200:
        raise HTTPException(
            status_code=missing_keywords_response.status_code,
            detail=f"Google API Error: {missing_keywords_response.text}",
        )

    try:
        missing_keywords_raw = missing_keywords_response.json()["candidates"][0][
            "content"
        ]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=500, detail="Unexpected response format from Google API"
        )

    # Normalize list-like output into comma-separated header value.
    missing_keywords = ", ".join(
        [
            line.strip(" -*\t")
            for line in missing_keywords_raw.splitlines()
            if line.strip(" -*\t")
        ]
    )

    response_headers = {}
    if missing_keywords:
        response_headers["x-ats-missing-keywords"] = missing_keywords
        print(f"ATS Missing Keywords:\n{missing_keywords}")

    return Response(
        content=pdf_bytes, media_type="application/pdf", headers=response_headers
    )


@router.post("/score")
async def score_resume(
    file: UploadFile = File(...),
    resume_text: str = Form(...),
    job_desc: str = Form(...),
):
    if file.filename and not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    if not job_desc.strip():
        raise HTTPException(status_code=400, detail="job_desc is required")

    try:
        content: bytes | None = await file.read() if file.filename else None
        score = ats_score_evaluator(
            job_desc=job_desc, pdf_bytes=content, resume_text=resume_text
        )
        return {"evaluation": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to score resume: {str(e)}")

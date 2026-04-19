from fastapi import APIRouter, HTTPException, Response, UploadFile, File, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from constants.latex_templates import templates
from utils.latex import latex_to_pdf
from utils.parsing import parse_file
from middleware.authMiddleware import verify_google_oauth_token, security
import requests
import os
import dotenv
import re
import urllib.parse
dotenv.load_dotenv()


class GenerateResumeRequestBody(BaseModel):
    user_info: str
    job_desc: str
    custom_instructions: str
    gemini_model: str = "gemini-2.5-flash"
    template_id: str | None = None
    template_latex: str | None = None


router = APIRouter()


@router.get("/latex-templates")
async def get_latex_templates(token_data: dict = Depends(verify_google_oauth_token)):

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


@router.post("/generate")
async def generate_resume(
    body: GenerateResumeRequestBody,
    token_data: dict = Depends(verify_google_oauth_token),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    gemini_model = body.gemini_model
    
    latex_template = None
    if body.template_id:
        template = next((t for t in templates if t["id"] == body.template_id), None)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        latex_template = template['latex']
    elif body.template_latex:
        latex_template = body.template_latex
    
    if not latex_template:
        raise HTTPException(status_code=400, detail="Either template_id or template_latex must be provided")

    final_prompt = f"""
    Use the given information to construct a finalized latex code followed by a cover letter. Your output format should be the following two code blocks ONLY:
    ```latex
    <The Latex Code>
    ```
    ```markdown
    <Cover Letter>
    ```
    
    YOU MUST NOT SAY ANYTHING ELSE.
    
    IMPORTANT RULES:
    1. Do not make changes in the code structure or stylistics in the latex code provided. Only update the content in the section. 
    2. Update the content using the user information and job description. Your result it going to be evaluated for ATS scores so make sure updates are relevant, clean and accurate.
    3. Remove any sections that are not applicable, or user information does not contain content enough to fill it.
    4. Do not add details not present in the user information.
    5. Ensure all special characters like `&` are escaped as `\&`.
    6. Do not include any other text outside the two code blocks.
    7. You may only make exception to these rules if additional instructions are provided.

    user infromation: {body.user_info}
    job description: {body.job_desc}
    additional instructions: {body.custom_instructions}
    template: {latex_template}
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
    try:
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Split into latex and cover letter sections
        latex_match = re.search(r'```latex\s*(.*?)\s*```', raw_text, re.DOTALL)
        markdown_match = re.search(r'```markdown\s*(.*?)\s*```', raw_text, re.DOTALL)

        generated_latex = latex_match.group(1).strip() if latex_match else ""
        generated_cover_letter = markdown_match.group(1).strip() if markdown_match else ""
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=500, detail="Unexpected response format from Google API"
        )

    print(f"generated_latex: {generated_latex}")
    print(f"generated_cover_letter: {generated_cover_letter}")


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
        # Use URL-encoding to avoid UnicodeEncodeError in headers
        response_headers["X-ATS-Missing-Keywords"] = urllib.parse.quote(missing_keywords)
        print(f"ATS Missing Keywords:\n{missing_keywords}")

    if generated_cover_letter:
        # Use URL-encoding to avoid UnicodeEncodeError in headers
        response_headers["X-Cover-Letter"] = urllib.parse.quote(generated_cover_letter)

    return Response(
        content=pdf_bytes, media_type="application/pdf", headers=response_headers
    )

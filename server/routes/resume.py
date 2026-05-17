from fastapi import APIRouter, HTTPException, Response, UploadFile, File, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from constants.latex_templates import templates
from utils.latex import latex_to_pdf
from utils.parsing import parse_file
from middleware.rateLimitMiddleware import rate_limit_middleware
from middleware.authMiddleware import verify_google_oauth_token
from middleware.authMiddleware import security
import requests
import os
import dotenv
import re
import urllib.parse
from constants.sys_prompt import SYS_PROMPT_FOR_LLM
from utils.cache_manager import request_cache
from utils.google_auth import get_google_auth_token
from utils.validations import validate_resume_generation_input
import httpx
dotenv.load_dotenv()


class GenerateResumeRequestBody(BaseModel):
    user_info: str
    job_desc: str
    custom_instructions: str | None = None
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
                "link": template["link"],
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
    token_data: dict = Depends(rate_limit_middleware),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    # Validate input
    validate_resume_generation_input(
        user_info=body.user_info,
        job_desc=body.job_desc,
        custom_instructions=body.custom_instructions,
        template_latex=body.template_latex
    )

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

    final_prompt = SYS_PROMPT_FOR_LLM.format(
        user_info=body.user_info,
        job_desc=body.job_desc,
        custom_instructions=body.custom_instructions,
        latex_template=latex_template
    )

    # check for model's per day project limit
    input_tokens = request_cache.estimate_input_tokens(final_prompt, gemini_model)
    model_limit = request_cache.get_model_remaining_tokens(gemini_model)
    
    if not model_limit:
        raise HTTPException(
            status_code=400,
            detail=f"Model {gemini_model} is not supported or pricing data is missing."
        )

    # we will use a ballpark estimate of 2500 output tokens that safely makes sure the request does not cross our project limits
    if model_limit["remaining_input_tokens"] - input_tokens <= 0 and model_limit["remaining_output_tokens"] - 2500 <= 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Model daily token budget reached. Please try again tomorrow.",
            headers={"x-rate-limit-flag": "true"}
        )


    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    
    token = credentials.credentials
    vertex_api_key = os.getenv("VERTEX_API_KEY")

    # Authenticate: Use API Key if available, otherwise use ADC (Service Account)
    auth_headers = {}
    if vertex_api_key:
        # For API key, project_id is often not needed, but we keep it if configured
        if project_id:
            auth_headers["x-goog-user-project"] = project_id
    else:
        try:
            adc_token, adc_project = get_google_auth_token()
            auth_headers["Authorization"] = f"Bearer {adc_token}"
            # x-goog-user-project is CRITICAL for ADC to identify the billing/quota project
            # We use the project from ADC if the environment variable is missing
            project_id = project_id or adc_project
            if project_id:
                auth_headers["x-goog-user-project"] = project_id
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to fetch ADC token: {str(e)}"
            )

    if not project_id and not vertex_api_key:
         raise HTTPException(
            status_code=500, detail="Project ID could not be determined for ADC. Set GOOGLE_CLOUD_PROJECT_ID."
        )

    # Vertex AI Platform endpoint
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/{gemini_model}:generateContent"
    if vertex_api_key:
        url += f"?key={vertex_api_key}"

    headers = {
        **auth_headers,
        "Content-Type": "application/json",
    }

    data = {
        "contents": [{"role": "user", "parts": [{"text": final_prompt}]}],
        "generationConfig": {
            "thinkingConfig": {
                "thinkingBudget": 0
            }
        }
    }

    
    total_input_tokens = 0
    total_output_tokens = 0

    async with httpx.AsyncClient(timeout=60.0) as client:
        ai_response = await client.post(url, headers=headers, json=data)
    
    if ai_response.status_code != 200:
        raise HTTPException(
            status_code=ai_response.status_code,
            detail=f"Google API Error: {ai_response.text}",
        )

    result = ai_response.json()
    usage = result.get("usageMetadata", {})
    total_input_tokens += usage.get("promptTokenCount", 0)
    total_output_tokens += usage.get("candidatesTokenCount", 0)

    try:
        candidate = result.get("candidates", [{}])[0]
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        
        # Robustly join all text parts (skipping thoughts or other non-text parts if present)
        raw_text = "".join([part.get("text", "") for part in parts]).strip()
        
        if not raw_text:
            finish_reason = candidate.get("finishReason", "UNKNOWN")
            raise HTTPException(
                status_code=500, 
                detail=f"Model returned no text. Finish reason: {finish_reason}"
            )

        # Split into latex and cover letter sections
        latex_match = re.search(r'```latex\s*(.*?)\s*```', raw_text, re.DOTALL)
        markdown_match = re.search(r'```markdown\s*(.*?)\s*```', raw_text, re.DOTALL)

        generated_latex = latex_match.group(1).strip() if latex_match else ""
        generated_cover_letter = markdown_match.group(1).strip() if markdown_match else ""
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=500, detail="Unexpected response format from Google API"
        )

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
        "contents": [{"role": "user", "parts": [{"text": missing_keywords_prompt}]}],
        "generationConfig": {
            "thinkingConfig": {
                "thinkingBudget": 0
            }
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        missing_keywords_response = await client.post(
            url, headers=headers, json=missing_keywords_data
        )

    if missing_keywords_response.status_code != 200:
        raise HTTPException(
            status_code=missing_keywords_response.status_code,
            detail=f"Google API Error: {missing_keywords_response.text}",
        )

    try:
        missing_keywords_result = missing_keywords_response.json()
        usage_kw = missing_keywords_result.get("usageMetadata", {})
        total_input_tokens += usage_kw.get("promptTokenCount", 0)
        total_output_tokens += usage_kw.get("candidatesTokenCount", 0)

        parts_kw = missing_keywords_result.get("candidates", [{}])[0].get("content", {}).get("parts", [])

        missing_keywords_raw = "".join([p.get("text", "") for p in parts_kw]).strip()
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

    # Update token budgets in cache
    request_cache.update_model_token_budget(
        gemini_model, 
        input_tokens=total_input_tokens, 
        output_tokens=total_output_tokens
    )

    response_headers = {}
    if missing_keywords:
        # Use URL-encoding to avoid UnicodeEncodeError in headers
        response_headers["X-ATS-Missing-Keywords"] = urllib.parse.quote(missing_keywords)

    if generated_cover_letter:
        # Use URL-encoding to avoid UnicodeEncodeError in headers
        response_headers["X-Cover-Letter"] = urllib.parse.quote(generated_cover_letter)

    return Response(
        content=pdf_bytes, media_type="application/pdf", headers=response_headers
    )

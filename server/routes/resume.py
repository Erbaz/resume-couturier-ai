from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from constants.latex_templates import templates
from utils.latex import latex_to_pdf

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
async def parse_resume():
    return {"message": "placeholder"}

@router.post("/generate/{template_id}")
async def generate_resume(template_id: str, body: GenerateResumeRequestBody):
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

    pdf_bytes = latex_to_pdf(template["latex"])
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.post("/score")
async def score_resume():
    return {"message": "placeholder"}

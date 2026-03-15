from fastapi import APIRouter, HTTPException, Response
from constants.latex_templates import templates
from utils.latex import latex_to_pdf

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
async def generate_resume(template_id: str):
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
        
    pdf_bytes = latex_to_pdf(template["latex"])
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.post("/score")
async def score_resume():
    return {"message": "placeholder"}

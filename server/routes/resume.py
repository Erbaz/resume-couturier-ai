from fastapi import APIRouter
from constants.latex_templates import templates

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

@router.post("/generate")
async def generate_resume():
    return {"message": "placeholder"}

@router.post("/score")
async def score_resume():
    return {"message": "placeholder"}

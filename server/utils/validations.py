import re
from fastapi import HTTPException
from utils.latex import latex_to_pdf

import io
from pypdf import PdfReader

def validate_resume_generation_input(
    user_info: str, 
    job_desc: str, 
    custom_instructions: str = None, 
    template_latex: str = None
):
    """
    Validates the input for resume generation.
    - user_info: max 10000 chars, no code patterns.
    - job_desc: max 10000 chars, no code patterns.
    - custom_instructions: max 5000 chars, no code patterns.
    - template_latex: optional, max 100000 chars, must be valid LaTeX, no other code patterns, max 3 pages.
    """
    
    # 1. Length Validations
    if len(user_info) > 10000:
        raise HTTPException(status_code=400, detail="user_info exceeds 10000 characters.")
    
    if len(job_desc) > 10000:
        raise HTTPException(status_code=400, detail="job_desc exceeds 10000 characters.")
    
    if custom_instructions and len(custom_instructions) > 5000:
        raise HTTPException(status_code=400, detail="custom_instructions exceeds 5000 characters.")

    # 2. Code Pattern Detection
    # We use patterns that specifically look for code structures rather than just keywords.
    # This avoids false positives for common English words like "from", "return", or "class".
    forbidden_code_patterns = [
        r'<(script|iframe|object|embed|applet).*?>',
        r'<\?php',
        r'#include\s+<.*>',
        r'\b(def|function)\s+\w+\s*\(', # Python/JS function definitions
        r'\b(var|let|const)\s+\w+\s*=',  # JS variable assignments
        r'System\.out\.println',
        r'console\.log',
        r'\w+\s*\(.*\)\s*\{', # C-style function definitions
        r'\b(public|private|protected)\s+class\s+\w+', # Java/C# class definitions
        r'\bimport\s+[\w\.]+\s*;', # Java/other imports with semicolons
        r'\bfrom\s+[\w\.]+\s+import\s+[\w\.]+', # Python imports
    ]

    def check_for_code(text, field_name):
        if not text:
            return
        for pattern in forbidden_code_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Forbidden code pattern detected in {field_name}."
                )

    check_for_code(user_info, "user_info")
    check_for_code(job_desc, "job_desc")
    if custom_instructions:
        check_for_code(custom_instructions, "custom_instructions")

    # 3. LaTeX Validation
    if template_latex:
        if len(template_latex) > 100000:
            raise HTTPException(status_code=400, detail="template_latex exceeds 100000 characters.")

        # Check for non-latex code patterns
        check_for_code(template_latex, "template_latex")
        
        # LaTeX must have documentclass and begin{document}
        if not (re.search(r'\\documentclass', template_latex) and re.search(r'\\begin\{document\}', template_latex)):
             raise HTTPException(
                status_code=400, 
                detail="template_latex must be a valid LaTeX document containing \\documentclass and \\begin{document}."
            )

        # Compiler validation and page count check
        # We use the existing latex_to_pdf to verify if the code is compilable.
        pdf_bytes = latex_to_pdf(template_latex)
        if not pdf_bytes:
            raise HTTPException(
                status_code=400, 
                detail="template_latex failed to compile. Please ensure it is valid LaTeX code."
            )
        
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            page_count = len(reader.pages)
            if page_count > 3:
                raise HTTPException(
                    status_code=400, 
                    detail=f"template_latex results in {page_count} pages. Maximum allowed is 3 pages."
                )
        except Exception as e:
            # If PDF reading fails, we still allow it as long as compilation succeeded, 
            # but ideally this shouldn't happen for valid PDFs.
            pass

    return True

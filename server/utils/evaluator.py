import os
import tempfile
import subprocess
from utils.parsing import parse_to_markdown

def ats_score_evaluator(pdf_bytes: bytes, job_desc: str) -> str:
    """
    Accepts a PDF file as bytes, converts it to Markdown using docling,
    and runs the ats-resume-scorer tool to generate a score against a job description.
    """
    markdown_text = parse_to_markdown(pdf_bytes, "resume.pdf")
    
    with tempfile.TemporaryDirectory() as tempdir:
        resume_txt_path = os.path.join(tempdir, "resume.txt")
        job_txt_path = os.path.join(tempdir, "job.txt")
        
        with open(resume_txt_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)
        
        with open(job_txt_path, "w", encoding="utf-8") as f:
            f.write(job_desc)
            
        process = subprocess.run(
            ["ats-score", "--resume", resume_txt_path, "--jd", job_txt_path, "--level", "normal"],
            capture_output=True,
            text=True
        )
        return process.stdout

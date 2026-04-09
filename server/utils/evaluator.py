import os
import tempfile
import subprocess


def ats_score_evaluator(job_desc: str, pdf_bytes: bytes = None, resume_text:str = None ) -> str:
    """
    Accepts a PDF file as bytes, writes it to a temporary PDF file,
    and runs the ats-resume-scorer tool to generate a score against a job description.
    """
    with tempfile.TemporaryDirectory() as tempdir:
        resume_pdf_path = os.path.join(tempdir, "resume.pdf")
        job_txt_path = os.path.join(tempdir, "job.txt")
        resume_text_path = os.path.join(tempdir, "resume_text.txt")

        if pdf_bytes:
            with open(resume_pdf_path, "wb") as f:
                f.write(pdf_bytes)

        if resume_text:
            with open(resume_text_path, "w", encoding="utf-8") as f:
                f.write(resume_text)

        with open(job_txt_path, "w", encoding="utf-8") as f:
            f.write(job_desc)

        process = subprocess.run(
            [
                "ats-score",
                "--resume",
                resume_pdf_path if pdf_bytes else resume_text_path,
                "--jd",
                job_txt_path,
                "--level",
                "normal",
            ],
            capture_output=True,
            text=True,
        )
        return process.stdout

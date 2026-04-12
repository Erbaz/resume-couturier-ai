import subprocess
import tempfile
import os

def latex_to_pdf(latex_code: str) -> bytes:
    with tempfile.TemporaryDirectory() as tempdir:
        tex_path = os.path.join(tempdir, "resume.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)
            
        try:
            process = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "resume.tex"],
                cwd=tempdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if process.returncode != 0:
                print("LaTeX Error Output:")
                print(process.stdout.decode("utf-8"))
                print(process.stderr.decode("utf-8"))
        except FileNotFoundError:
            print("Error: pdflatex is not installed or not in your system PATH.")
            return b""
        
        pdf_path = os.path.join(tempdir, "resume.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                return f.read()
            
    return b""

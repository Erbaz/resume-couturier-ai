import io
import os
from pypdf import PdfReader
from docx import Document


def parse_to_markdown(file_bytes: bytes, filename: str) -> str:
    """
    Parses a PDF or DOCX file (provided as bytes) and returns a Markdown-like plain text body.
    """
    ext = os.path.splitext(filename.lower())[1]

    if ext == ".pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []
        for page in reader.pages:
            text = (page.extract_text() or "").strip()
            if text:
                pages.append(text)
        print(" ----parsed pdf text----")
        print("\n\n".join(pages))
        return "\n\n".join(pages)

    if ext == ".docx":
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = []
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                paragraphs.append(text)
        return "\n\n".join(paragraphs)

    raise ValueError(f"Unsupported file extension: {ext}")

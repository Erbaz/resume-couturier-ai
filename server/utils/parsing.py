import os
import tempfile
from docling.document_converter import DocumentConverter
def parse_to_markdown(file_bytes: bytes, filename: str) -> str:
    """
    Parses a PDF or DOCX file (provided as bytes) and returns its content as a Markdown string using docling.
    """
    ext = os.path.splitext(filename)[1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:
        converter = DocumentConverter()
        result = converter.convert_single(temp_path)
        markdown_text = result.output.export_to_markdown()
        return markdown_text
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

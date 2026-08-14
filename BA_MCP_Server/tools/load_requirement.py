from pathlib import Path

import PyPDF2
from docx import Document

from observability.logger import log_event
from observability.trace import generate_trace_id, set_trace_id


def load_requirement(file_name: str, trace_id: str = "") -> str:
    """Load requirement document"""
    set_trace_id(trace_id or generate_trace_id())
    log_event("mcp", f"load_requirement called file_name='{file_name}'")

    base_path = Path(__file__).parent.parent / "requirements"

    file_path = base_path / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Requirement file not found: {file_name}")

    suffix = file_path.suffix.lower()

    if suffix == ".txt":
        return _extract_txt(file_path)
    if suffix == ".pdf":
        return _extract_pdf(file_path)
    if suffix == ".docx":
        return _extract_docx(file_path)

    raise ValueError(f"Unsupported file format: {suffix}")


def _extract_txt(path: Path):

    return path.read_text(encoding="utf-8")


def _extract_pdf(path: Path):

    text = ""
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def _extract_docx(path: Path):

    doc = Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

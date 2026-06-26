from __future__ import annotations
import io
from app.core.exceptions import DocumentParsingError, UnsupportedFileTypeError
from app.core.logging import get_logger

logger = get_logger(__name__)

SUPPORTED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}


async def parse_document(file_bytes: bytes, content_type: str, filename: str) -> str:
    if content_type not in SUPPORTED_TYPES:
        raise UnsupportedFileTypeError(f"Unsupported file type: {content_type}")

    try:
        if content_type == "application/pdf":
            return _parse_pdf(file_bytes)
        elif "wordprocessingml" in content_type:
            return _parse_docx(file_bytes)
        else:
            return _parse_text(file_bytes)
    except (UnsupportedFileTypeError, DocumentParsingError):
        raise
    except Exception as exc:
        raise DocumentParsingError(f"Failed to parse {filename}: {exc}") from exc


def _parse_pdf(data: bytes) -> str:
    import pypdf

    reader = pypdf.PdfReader(io.BytesIO(data))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def _parse_docx(data: bytes) -> str:
    import docx

    doc = docx.Document(io.BytesIO(data))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def _parse_text(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")

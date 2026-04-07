from pathlib import Path
from .text import extract as _extract_text
from .md import extract as _extract_md
from .pdf import extract as _extract_pdf
from .docx import extract as _extract_docx

_EXTRACTORS = {
    'text': _extract_text,
    'md': _extract_md,
    'pdf': _extract_pdf,
    'docx': _extract_docx,
}


def extract(file_path: Path, fmt: str) -> str:
    return _EXTRACTORS[fmt](file_path)

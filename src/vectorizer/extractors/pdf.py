import re
from pathlib import Path
from pypdf import PdfReader


def _clean(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def extract(file_path: Path) -> str:
    reader = PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ''
        text = _clean(text)
        if text:
            pages.append(f"[Page {i}]\n{text}")
    return '\n\n'.join(pages)

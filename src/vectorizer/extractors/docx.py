from pathlib import Path
from docx import Document

_HEADING_PREFIX = {
    'Heading 1': '#',
    'Heading 2': '##',
    'Heading 3': '###',
    'Heading 4': '####',
}


def extract(file_path: Path) -> str:
    doc = Document(file_path)
    lines = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        prefix = _HEADING_PREFIX.get(para.style.name)
        lines.append(f"{prefix} {text}" if prefix else text)
    return '\n\n'.join(lines)

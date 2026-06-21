import re


def chunk_by_words(text: str, chunk_size: int, overlap: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(' '.join(words[start:end]))
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks


def chunk_by_sections(text: str) -> list[str]:
    # Start a new section at any Markdown heading (# .. ######) so DOCX
    # 'Heading 1' (rendered as '# ') splits like 'Heading 2' ('## ').
    parts = re.split(r'(?=^#{1,6} )', text, flags=re.MULTILINE)
    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        return []
    # Merge any preamble (text before the first heading) into the first section.
    if not parts[0].startswith('#') and len(parts) > 1:
        parts[1] = parts[0] + '\n\n' + parts[1]
        parts = parts[1:]
    return parts

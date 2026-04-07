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
    parts = re.split(r'(?=^## )', text, flags=re.MULTILINE)
    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        return []
    if parts and not parts[0].startswith('## ') and len(parts) > 1:
        parts[1] = parts[0] + '\n\n' + parts[1]
        parts = parts[1:]
    return parts

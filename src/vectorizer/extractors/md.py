from pathlib import Path


def extract(file_path: Path) -> str:
    return file_path.read_text(encoding='utf-8')

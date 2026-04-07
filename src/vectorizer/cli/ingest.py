import argparse
import asyncio
import sys
from pathlib import Path
from vectorizer import settings
from vectorizer.ingest import ingest


def main():
    parser = argparse.ArgumentParser(description='Ingest a text file into the RAG knowledge base via MCP.')
    parser.add_argument('file', help='path to the text file to ingest')
    parser.add_argument('--source', default='files', help='source tag for filtering (default: files)')
    parser.add_argument('--title', help='document title (default: file name)')
    parser.add_argument('--mcp-url', help=f'MCP server URL (default: {settings.mcp_url})')
    parser.add_argument('--collection', help='collection name (default: from settings)')
    parser.add_argument('--format', choices=['text', 'md', 'pdf', 'docx'], default=None, help='document format (default: derived from file extension, fallback: text)')
    parser.add_argument('--no-split', action='store_true', help='store the entire document as a single chunk without splitting')
    parser.add_argument('--chunk-size', type=int, default=None, help=f'chunk size in words, used for text format (default: {settings.chunk_size})')
    parser.add_argument('--overlap', type=int, default=None, help=f'overlap in words between chunks, used for text format (default: {settings.chunk_overlap})')
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    if args.mcp_url:
        settings.mcp_url = args.mcp_url
    if args.collection:
        settings.collection = args.collection

    title = args.title or file_path.name
    _EXT_FORMAT = {'.pdf': 'pdf', '.md': 'md', '.markdown': 'md', '.docx': 'docx'}
    fmt = args.format or _EXT_FORMAT.get(file_path.suffix.lower(), 'text')
    split_by = 'sections' if fmt in ('md', 'docx') else 'words'
    chunk_size = 0 if args.no_split else (args.chunk_size or settings.chunk_size)
    overlap = args.overlap or settings.chunk_overlap
    asyncio.run(ingest(file_path, source=args.source, title=title, chunk_size=chunk_size, overlap=overlap, split_by=split_by, fmt=fmt))

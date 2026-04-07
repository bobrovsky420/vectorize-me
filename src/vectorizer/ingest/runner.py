from pathlib import Path
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
from vectorizer import settings
from vectorizer.extractors import extract
from .chunking import chunk_by_words, chunk_by_sections


async def _store_chunk(session: ClientSession, text: str, metadata: dict):
    args = {'information': text, 'metadata': metadata}
    if settings.collection:
        args['collection_name'] = settings.collection
    await session.call_tool(settings.mcp_tool.replace('find', 'store'), args)


async def ingest(file_path: Path, source: str, title: str, chunk_size: int, overlap: int, split_by: str, fmt: str):
    text = extract(file_path, fmt)

    if chunk_size == 0:
        chunks = None
    elif split_by == 'sections':
        chunks = chunk_by_sections(text)
    else:
        chunks = chunk_by_words(text, chunk_size, overlap)

    async with streamable_http_client(settings.mcp_url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if not chunks or len(chunks) <= 1:
                await _store_chunk(session, text, {'source': source, 'title': title})
                print(f"Stored: {file_path} (1 chunk)")
            else:
                total = len(chunks)
                for i, chunk in enumerate(chunks, 1):
                    metadata = {'source': source, 'title': title, 'chunk': i, 'total_chunks': total}
                    await _store_chunk(session, chunk, metadata)
                    print(f"Stored chunk {i}/{total}", end='\r')
                print(f"Stored: {file_path} ({total} chunks, split-by={split_by})")

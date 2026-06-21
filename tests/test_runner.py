import asyncio
from pathlib import Path

import pytest

import vectorizer.ingest.runner as runner
from vectorizer import settings


class _FakeSession:
    last = None

    def __init__(self, read, write):
        self.calls = []
        _FakeSession.last = self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def initialize(self):
        pass

    async def call_tool(self, name, args):
        self.calls.append((name, args))


class _FakeHTTP:
    async def __aenter__(self):
        return ('read', 'write', 'extra')

    async def __aexit__(self, *exc):
        return False


@pytest.fixture(autouse=True)
def patch_mcp(monkeypatch):
    monkeypatch.setattr(runner, 'streamable_http_client', lambda url: _FakeHTTP())
    monkeypatch.setattr(runner, 'ClientSession', _FakeSession)
    monkeypatch.setattr(runner, 'extract', lambda path, fmt: 'one two three four five six')
    monkeypatch.setattr(settings, 'mcp_store_tool', 'qdrant-store')
    monkeypatch.setattr(settings, 'mcp_url', 'http://x')
    monkeypatch.setattr(settings, 'collection', None)


def _run(**kwargs):
    base = dict(
        file_path=Path('doc.txt'), source='files', title='doc.txt',
        chunk_size=0, overlap=0, split_by='words', fmt='text',
    )
    base.update(kwargs)
    asyncio.run(runner.ingest(**base))
    return _FakeSession.last.calls


def test_single_chunk_when_no_split(capsys):
    calls = _run(chunk_size=0)
    assert len(calls) == 1
    name, args = calls[0]
    assert name == 'qdrant-store'
    assert args['information'] == 'one two three four five six'
    assert args['metadata'] == {'source': 'files', 'title': 'doc.txt'}
    assert 'collection_name' not in args
    assert '1 chunk' in capsys.readouterr().out


def test_word_split_into_multiple_chunks():
    calls = _run(chunk_size=2, overlap=0, split_by='words')
    assert len(calls) == 3
    _, first = calls[0]
    assert first['metadata'] == {'source': 'files', 'title': 'doc.txt', 'chunk': 1, 'total_chunks': 3}


def test_section_split(monkeypatch):
    monkeypatch.setattr(runner, 'extract', lambda path, fmt: '# A\nx\n\n# B\ny')
    calls = _run(chunk_size=10, split_by='sections')
    assert [a['information'] for _, a in calls] == ['# A\nx', '# B\ny']


def test_collection_name_included(monkeypatch):
    monkeypatch.setattr(settings, 'collection', 'mycol')
    calls = _run(chunk_size=0)
    assert calls[0][1]['collection_name'] == 'mycol'

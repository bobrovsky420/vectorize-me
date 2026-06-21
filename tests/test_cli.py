import pytest

import vectorizer.cli.ingest as cli
from vectorizer import settings


@pytest.fixture
def captured(monkeypatch):
    """Replace the async ingest() with a recorder and return the captured kwargs."""
    recorded = {}

    async def fake_ingest(file_path, **kwargs):
        recorded['file_path'] = file_path
        recorded.update(kwargs)

    monkeypatch.setattr(cli, 'ingest', fake_ingest)
    return recorded


def _argv(monkeypatch, *args):
    monkeypatch.setattr('sys.argv', ['mcp-ingest', *args])


def test_missing_file_exits(monkeypatch, capsys):
    _argv(monkeypatch, 'nope.txt')
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 1
    assert 'File not found' in capsys.readouterr().out


def test_format_derived_from_extension(monkeypatch, captured, tmp_path):
    f = tmp_path / 'paper.pdf'
    f.write_bytes(b'%PDF-1.4')
    _argv(monkeypatch, str(f))
    cli.main()
    assert captured['fmt'] == 'pdf'
    assert captured['split_by'] == 'words'
    assert captured['title'] == 'paper.pdf'


def test_docx_defaults_to_sections(monkeypatch, captured, tmp_path):
    f = tmp_path / 'spec.docx'
    f.write_bytes(b'PK')
    _argv(monkeypatch, str(f))
    cli.main()
    assert captured['fmt'] == 'docx'
    assert captured['split_by'] == 'sections'


def test_unknown_extension_falls_back_to_text(monkeypatch, captured, tmp_path):
    f = tmp_path / 'data.xyz'
    f.write_text('x', encoding='utf-8')
    _argv(monkeypatch, str(f))
    cli.main()
    assert captured['fmt'] == 'text'


def test_no_split_sets_chunk_size_zero(monkeypatch, captured, tmp_path):
    f = tmp_path / 'a.txt'
    f.write_text('x', encoding='utf-8')
    _argv(monkeypatch, str(f), '--no-split')
    cli.main()
    assert captured['chunk_size'] == 0


def test_overrides_and_title(monkeypatch, captured, tmp_path):
    f = tmp_path / 'a.txt'
    f.write_text('x', encoding='utf-8')
    _argv(
        monkeypatch, str(f),
        '--title', 'Custom', '--source', 'wiki',
        '--mcp-url', 'http://host/mcp', '--collection', 'col',
        '--chunk-size', '0', '--overlap', '0',
    )
    cli.main()
    assert captured['title'] == 'Custom'
    assert captured['source'] == 'wiki'
    # explicit 0 must be honored, not replaced by the settings default
    assert captured['chunk_size'] == 0
    assert captured['overlap'] == 0
    assert settings.mcp_url == 'http://host/mcp'
    assert settings.collection == 'col'

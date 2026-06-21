import importlib
from pathlib import Path

# vectorizer/__init__ binds the `settings` instance over the submodule name,
# so reach the actual module object through importlib.
settings_module = importlib.import_module('vectorizer.settings')
Settings = settings_module.Settings
_load = settings_module._load


def test_defaults_when_data_empty():
    s = Settings({})
    assert s.mcp_url is None
    assert s.mcp_tool is None
    assert s.mcp_store_tool is None
    assert s.chunk_size == 512
    assert s.chunk_overlap == 64


def test_store_tool_derived_from_mcp_tool():
    s = Settings({'mcp_tool': 'qdrant-find'})
    assert s.mcp_store_tool == 'qdrant-store'


def test_store_tool_explicit_overrides_derivation():
    s = Settings({'mcp_tool': 'qdrant-find', 'mcp_store_tool': 'custom-store'})
    assert s.mcp_store_tool == 'custom-store'


def test_load_reads_yaml(tmp_path, monkeypatch):
    cfg = tmp_path / 'settings.yaml'
    cfg.write_text('mcp_url: http://x\nchunk_size: 10\n', encoding='utf-8')
    monkeypatch.setattr(settings_module, '_SETTINGS_FILE', cfg)
    s = _load()
    assert s.mcp_url == 'http://x'
    assert s.chunk_size == 10


def test_load_missing_file_uses_defaults(monkeypatch):
    monkeypatch.setattr(settings_module, '_SETTINGS_FILE', Path('does-not-exist.yaml'))
    s = _load()
    assert s.chunk_size == 512

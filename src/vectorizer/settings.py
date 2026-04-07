from pathlib import Path
import yaml

_SETTINGS_FILE = Path(__file__).parents[3] / 'settings.yaml'


class Settings:
    def __init__(self, data: dict):
        self.mcp_url: str = data.get('mcp_url')
        self.mcp_tool: str = data.get('mcp_tool')
        self.collection: str = data.get('collection')
        self.chunk_size: int = data.get('chunk_size', 512)
        self.chunk_overlap: int = data.get('chunk_overlap', 64)


def _load() -> Settings:
    if _SETTINGS_FILE.exists():
        data = yaml.safe_load(_SETTINGS_FILE.read_text(encoding='utf-8')) or {}
    else:
        data = {}
    return Settings(data)


settings = _load()

# vectorize-me

A small CLI for **MyDevTeam** that ingests documents into a RAG knowledge base over [MCP](https://modelcontextprotocol.io/). It extracts text from a file, splits it into chunks, and stores each chunk (with metadata) by calling an MCP server's `store` tool — designed for [`mcp-server-qdrant`](https://github.com/qdrant/mcp-server-qdrant).

## Features

- **Formats:** plain text, Markdown, PDF (`pypdf`), DOCX (`python-docx`).
- **Heading-aware DOCX:** `Heading 1–4` styles become Markdown prefixes (`#`–`####`); DOCX defaults to section-based chunking.
- **Cleaned PDF:** whitespace collapsed; each page prefixed with `[Page N]` for traceability.
- **Chunking:** word-based sliding window with overlap, Markdown section splitting, or no split (single chunk).
- **Configurable** via `settings.yaml` or CLI flags.

## Requirements

- Python ≥ 3.14
- A running MCP server exposing a `store` tool (e.g. `mcp-server-qdrant`)

## Install

```bash
pip install .
```

This installs the `mcp-ingest` command.

## Configuration

Defaults live in `settings.yaml`:

```yaml
mcp_url: http://localhost:8000/mcp   # MCP server endpoint (streamable HTTP)
mcp_tool: qdrant-find                # search tool name
mcp_store_tool: qdrant-store         # tool used to store chunks (derived from mcp_tool if omitted)
collection: null                     # collection name (null = server default)
chunk_size: 512                      # words per chunk
chunk_overlap: 64                    # overlapping words between chunks
```

CLI flags (`--mcp-url`, `--collection`, `--chunk-size`, `--overlap`) override these per run.

## Usage

```bash
mcp-ingest <file> [options]
```

| Option | Description |
| --- | --- |
| `--source` | Source tag for filtering (default: `files`) |
| `--title` | Document title (default: file name) |
| `--mcp-url` | MCP server URL |
| `--collection` | Target collection name |
| `--format` | `text` \| `md` \| `pdf` \| `docx` (default: from extension, fallback `text`) |
| `--no-split` | Store the whole document as one chunk |
| `--chunk-size` | Words per chunk (word splitting only) |
| `--overlap` | Overlap in words between chunks |

### Examples

```bash
# Ingest a PDF (page-prefixed, word-chunked)
mcp-ingest report.pdf --source docs --collection knowledge

# Ingest a DOCX, one chunk per heading section (the default for .docx)
mcp-ingest spec.docx

# Store a file as a single chunk
mcp-ingest notes.md --no-split
```

Format is derived from the extension (`.pdf`, `.md`/`.markdown`, `.docx`); everything else is treated as text. Markdown and DOCX default to **section** chunking (one chunk per Markdown heading, `#`–`######`); other formats use **word** chunking.

## Development

```bash
pip install -r requirements.txt -r requirements-dev.txt   # pytest, pylint
```

Source lives under `src/vectorizer/`:

- `cli/` — argument parsing and entry point
- `extractors/` — per-format text extraction (`text`, `md`, `pdf`, `docx`)
- `ingest/` — chunking strategies and the MCP store runner
- `settings.py` — `settings.yaml` loader

## License

[Apache-2.0](LICENSE)

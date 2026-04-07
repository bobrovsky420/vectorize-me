# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-04-07

### 🚀 Added

* **Heading-aware DOCX extraction:** Paragraph styles (`Heading 1-4`) are converted to Markdown prefixes (`#`/`##`/`###`/`####`), preserving document structure. DOCX files now default to `--split-by sections`, producing one chunk per heading section.

* **Cleaned PDF extraction:** Extracted text is normalised - excess whitespace and newlines are collapsed. Each page is prefixed with `[Page N]` for traceability in retrieved chunks.

## [0.1.0] - 2026-04-05

### 🚀 Added

* **Initial release:** CLI tool `mcp-ingest` for ingesting documents into a RAG knowledge base via MCP.
* **Format support:** Plain text, Markdown, PDF (`pypdf`) and DOCX (`python-docx`).
* **Chunking strategies:** Word-based sliding window (`--split-by words`) and Markdown section-based (`--split-by sections`). `--no-split` stores the document as a single chunk.
* **Configurable via `settings.yaml`:** MCP URL, tool name, collection name, default chunk size and overlap.

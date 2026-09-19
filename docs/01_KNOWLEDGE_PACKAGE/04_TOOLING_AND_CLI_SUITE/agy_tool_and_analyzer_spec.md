# 🛠️ AGY-TOOL & Autonomous Tooling Specification
**Suite Name:** `agy-tool` & `gemini-deep-analyzer`
**Author:** Fayzillo Ummatov

## 1. `agy-tool` CLI Overview
A custom high-performance CLI utility designed to reduce AI context token consumption by 85-95% while speeding up code inspection by 30x.

### Key Subcommand Modules:
- **`agy-tool code blueprint <path>`**:
  - Extracts classes, methods, signatures, and docstrings via AST without reading entire file bodies.
- **`agy-tool code endpoints <path>`**:
  - Automatically identifies NestJS/Express/FastAPI routes, HTTP methods, decorators, and DTO types.
- **`agy-tool secure scan <path>` & `redact <path>`**:
  - Scans and automatically sanitizes API keys, JWT tokens, IP addresses, and private passwords before sharing code.
- **`agy-tool session list/inspect/export`**:
  - Analyzes AI agent transcripts, token ROI, tool execution times, and conversation graphs.

## 2. `gemini-deep-analyzer`
- Leverages Gemini 2.5 Pro's 2M-token context window to perform full-repository static code analysis, architectural debt checks, and multimodal asset processing.

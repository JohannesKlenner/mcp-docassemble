# MCP Docassemble Server

A Model Context Protocol (MCP) server that exposes the complete Docassemble API surface to LLM clients. The server wraps 60+ endpoints and presents them as MCP tools so agents can manage users, interviews, packages, and configuration through a single integration point.

## Key Features
- Full Docassemble coverage with structured tool metadata for every endpoint.
- Hardened async MCP server implementation with environment-based configuration.
- Typed client library with graceful fallbacks for partially supported Docassemble installations.
- Command line interface for serving the MCP endpoint and checking Docassemble connectivity.
- Test suite that runs offline sanity checks by default and can exercise live Docassemble instances on demand.

## Requirements
- Python 3.10+
- Access to a Docassemble instance and API key when running integration workflows
- Optional: Docker and Docker Compose for containerised deployments

## Installation
```bash
pip install .
```

For development installs (adds linting and test tooling):

```bash
pip install '.[dev]'
```

## Configuration
Set the following environment variables before starting the MCP server:

- `DOCASSEMBLE_BASE_URL`: Base URL of the Docassemble deployment (for example `https://docassemble.example.com`).
- `DOCASSEMBLE_API_KEY`: API key with sufficient privileges.

You can copy `.env.example` to `.env` and customise it locally.

## Usage
Serve the MCP endpoint:

```bash
mcp-docassemble serve
```

Smoke-test the Docassemble connection from the CLI:

```bash
mcp-docassemble test-connection --base-url https://docassemble.example.com --api-key YOUR_KEY
```

## Testing
The default test run exercises only offline sanity checks:

```bash
pytest tests/test_sanity.py -v
```

Set `MCP_DOCASSEMBLE_LIVE_TESTS=1` to opt into the full suite, which requires a reachable Docassemble server with valid credentials.

## Docker
The repository contains a multi-stage `Dockerfile` and a development variant. The GitHub Actions workflow builds a hardened image and publishes it to GHCR. Locally you can build the image with:

```bash
docker build -t mcp-docassemble:latest .
```

Provide the required Docassemble environment variables at runtime:

```bash
docker run --rm \
  -e DOCASSEMBLE_BASE_URL=https://docassemble.example.com \
  -e DOCASSEMBLE_API_KEY=YOUR_KEY \
  mcp-docassemble:latest
```

## Project Structure
- `src/mcp_docassemble/`: MCP server, client, CLI, and helpers.
- `tests/`: Pytest-based suite with offline sanity checks and optional integration tests.
- `.github/workflows/`: CI pipeline that runs tests, scans, and builds the Docker image.
- `Dockerfile`, `Dockerfile.dev`: Production and development container definitions.

## Contributing
1. Create a feature branch.
2. Run `pytest tests/test_sanity.py` before pushing.
3. Use `black` and `isort` (installed via the `dev` extra) to keep formatting consistent.

## License
Released under the MIT License. See `LICENSE` for details.

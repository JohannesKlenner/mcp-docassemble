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
### Offline sanity checks
The default automated run exercises only the fast, offline sanity check:

```bash
pytest tests/test_sanity.py -v
```

### Live endpoint validation
When a Docassemble instance is reachable you can exercise every MCP tool via the helper script:

```bash
export DOCASSEMBLE_BASE_URL="https://docassemble.example.com"
export DOCASSEMBLE_API_KEY="YOUR_KEY"
export PYTHONIOENCODING="utf-8"
python scripts/run_live_endpoint_checks.py
```

The script waits between requests, mirrors the manual workflow we used for acceptance testing and stores a machine-readable summary in `live_test_results.json`.

#### Latest live test run (17 Sep 2025)
The suite touched 42 endpoints; 34 responded as expected. The remaining calls require additional server configuration (credentials, reale Sessions oder vorbereitete Ressourcen) und lieferten daher die dokumentierten Fehler unten.

| Kategorie | Erfolgreich | Gesamt | Hinweise zu offenen Punkten |
|-----------|-------------|--------|-----------------------------|
| Benutzer-Management | 12 | 12 | Alle Aufrufe erfolgreich (inkl. Benutzeranlage und Rechteverwaltung). |
| Daten & API-Keys | 4 | 5 | `retrieve_stashed_data` benötigt einen zuvor erzeugten Stash-Key. |
| Interview-Management | 8 | 12 | `run_interview_action` (501 `KeyError: 'save_status'`), `go_back_in_interview` (fehlende Session), `get_user_secret` & `get_login_url` erfordern gültige Benutzer-Credentials. |
| Playground-Management | 4 | 6 | `create_playground_project`/`delete_playground_project` liefern 404, solange keine Playground-Projekte vorhanden sind. |
| Server-Management | 6 | 7 | `uninstall_package` schlägt erwartungsgemäß fehl, wenn das Ziel-Package nicht installiert ist. |

Nutze die JSON-Zusammenfassung, um Regressionen zu verfolgen oder die erwartbaren Fehler zu whitelisten, bis der Docassemble-Server die fehlenden Voraussetzungen bereitstellt.

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

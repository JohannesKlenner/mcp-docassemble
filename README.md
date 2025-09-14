# MCP Docassemble Server

A Model Context Protocol (MCP) server that provides complete access to the Docassemble API for Large Language Models.

## Overview

This MCP server exposes all 61 Docassemble API endpoints, enabling comprehensive LLM integration with Docassemble systems. All available functions are clearly documented with required parameters and permissions.

## Features

### User Management
- Create, update, and manage users
- Handle user roles and permissions
- API key management

### Interview Management
- Start and manage interview sessions
- Set and read interview variables
- Execute interview actions
- Session management and navigation

### Playground Functions
- Upload and download files to/from playground
- Create and manage projects
- Install and manage packages

### System Administration
- Manage server configuration
- Package installation and updates
- System restart and monitoring
- Cache management

### File Operations
- Template field extraction
- File upload and download
- Markdown conversion
- Temporary data storage

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/your-username/mcp-docassemble.git
cd mcp-docassemble
```

2. Install dependencies:
```bash
pip install -e .
```

### Via Package Manager (when published)

```bash
pip install mcp-docassemble
```

## Configuration

### Environment Variables

Create a `.env` file or set the following environment variables:

```bash
DOCASSEMBLE_BASE_URL=https://your-docassemble-server.com
DOCASSEMBLE_API_KEY=your-api-key-here

# Optional settings
DOCASSEMBLE_TIMEOUT=30
DOCASSEMBLE_LOG_LEVEL=INFO
```

### Example .env file

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your Docassemble server details
```

## Usage

### Start the MCP Server

```bash
python -m mcp_docassemble
```

### Using with MCP-compatible Clients

Configure your MCP client to connect to this server. The server will automatically load configuration from `.env` file or environment variables.

## API Endpoints

The server provides all 61 Docassemble API endpoints, categorized as:

- **User Management** (9 endpoints): User creation, updates, deletion, info retrieval
- **Permissions** (4 endpoints): Role management, privilege granting/checking
- **Interview Sessions** (12 endpoints): Session lifecycle, variable management, navigation
- **Interview Operations** (8 endpoints): Interview actions, template operations
- **Playground** (9 endpoints): File management, project operations, package handling
- **System Administration** (8 endpoints): Server config, package installation, restarts
- **API Key Management** (8 endpoints): API key lifecycle and permissions
- **File Operations** (3 endpoints): Template fields, file processing, data storage

Each endpoint is fully documented with:
- Required parameters and data types
- Optional parameters with defaults
- Required permissions/privileges
- Usage examples
- Error handling and response formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This software is provided "as is" without warranty of any kind. Use at your own risk.

## Requirements

- Python 3.8+
- Access to a Docassemble server
- Valid Docassemble API key with appropriate permissions

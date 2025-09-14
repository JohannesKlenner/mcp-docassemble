# Setup Instructions

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/mcp-docassemble.git
   cd mcp-docassemble
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Docassemble server details
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Run the server:**
   ```bash
   python -m mcp_docassemble
   ```

## Configuration Details

### Required Settings

- `DOCASSEMBLE_BASE_URL`: Your Docassemble server URL (e.g., https://docassemble.example.com)
- `DOCASSEMBLE_API_KEY`: Your API key from Docassemble

### Optional Settings

- `DOCASSEMBLE_TIMEOUT`: Request timeout in seconds (default: 30)
- `DOCASSEMBLE_LOG_LEVEL`: Logging level (default: INFO)

### Getting an API Key

1. Log into your Docassemble server
2. Go to "My Account" → "API Keys"
3. Generate a new API key with appropriate permissions
4. Copy the key to your `.env` file

## Development Setup

1. **Install in development mode:**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run tests (if available):**
   ```bash
   pytest
   ```

3. **Format code:**
   ```bash
   black src/
   ```

## Troubleshooting

### Common Issues

1. **Connection errors**: Verify your `DOCASSEMBLE_BASE_URL` and API key
2. **Permission errors**: Ensure your API key has the required privileges
3. **Module not found**: Make sure you installed the package with `pip install -e .`

### Debug Mode

Set `DOCASSEMBLE_LOG_LEVEL=DEBUG` in your `.env` file for detailed logging.

## Security Notes

- Never commit your `.env` file to version control
- Use environment-specific API keys
- Regularly rotate your API keys
- Review API key permissions regularly

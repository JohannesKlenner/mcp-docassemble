#!/usr/bin/env python3
"""
MCP Docassemble Server - Hauptausführungsscript

Startet den Docassemble MCP Server mit Konfiguration über Umgebungsvariablen.

Erforderliche Umgebungsvariablen:
- DOCASSEMBLE_BASE_URL: Base URL der Docassemble Installation (z.B. https://docassemble.example.com)
- DOCASSEMBLE_API_KEY: API Key für Authentifizierung

Verwendung:
    python -m mcp_docassemble.main
    
Oder direkt:
    python main.py
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add src directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_docassemble import create_server


def setup_logging():
    """Konfiguriert Logging für den MCP Server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr),
        ]
    )


def validate_environment():
    """Validiert erforderliche Umgebungsvariablen"""
    required_vars = {
        'DOCASSEMBLE_BASE_URL': 'Base URL der Docassemble Installation',
        'DOCASSEMBLE_API_KEY': 'API Key für Authentifizierung'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  {var}: {description}")
    
    if missing_vars:
        print("Fehler: Erforderliche Umgebungsvariablen fehlen:", file=sys.stderr)
        print("\n".join(missing_vars), file=sys.stderr)
        print("\nBeispiel:", file=sys.stderr)
        print("export DOCASSEMBLE_BASE_URL=https://docassemble.example.com", file=sys.stderr)
        print("export DOCASSEMBLE_API_KEY=your_api_key_here", file=sys.stderr)
        sys.exit(1)


async def main():
    """Hauptfunktion - startet den MCP Server"""
    setup_logging()
    validate_environment()
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starte Docassemble MCP Server...")
        server = create_server()
        await server.run()
        
    except KeyboardInterrupt:
        logger.info("Server durch Benutzer gestoppt")
        
    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

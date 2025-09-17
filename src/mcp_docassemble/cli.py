#!/usr/bin/env python3
"""
MCP Docassemble Server - Command Line Interface

Kommandozeilenschnittstelle für den Docassemble MCP Server.

Verwendung:
    mcp-docassemble --help
    mcp-docassemble serve
    mcp-docassemble test-connection
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional

from .client import DocassembleAPIError, DocassembleClient
from .main import main as run_server
from .main import setup_logging, validate_environment


def test_connection(base_url: str, api_key: str) -> bool:
    """Testet die Verbindung zur Docassemble API"""
    try:
        client = DocassembleClient(base_url, api_key)
        result = client.get_current_user()
        print(
            f"✅ Verbindung erfolgreich! Angemeldet als: {result.get('email', 'Unbekannt')}"
        )
        print(f"   Benutzer ID: {result.get('id', 'Unbekannt')}")
        print(f"   Berechtigungen: {', '.join(result.get('privileges', []))}")
        return True

    except DocassembleAPIError as e:
        print(f"❌ API Fehler: {e}")
        if e.status_code:
            print(f"   HTTP Status: {e.status_code}")
        return False

    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
        return False


async def serve_command(args):
    """Startet den MCP Server"""
    await run_server()


def test_command(args):
    """Testet die Verbindung zur Docassemble API"""
    base_url = args.base_url or os.getenv("DOCASSEMBLE_BASE_URL")
    api_key = args.api_key or os.getenv("DOCASSEMBLE_API_KEY")

    if not base_url:
        print(
            "❌ Fehler: DOCASSEMBLE_BASE_URL fehlt (--base-url oder Umgebungsvariable)",
            file=sys.stderr,
        )
        sys.exit(1)

    if not api_key:
        print(
            "❌ Fehler: DOCASSEMBLE_API_KEY fehlt (--api-key oder Umgebungsvariable)",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"🔄 Teste Verbindung zu {base_url}...")
    success = test_connection(base_url, api_key)

    if not success:
        print("\n💡 Überprüfe:")
        print("   • Base URL ist korrekt und erreichbar")
        print("   • API Key ist gültig und nicht abgelaufen")
        print("   • Docassemble Server läuft und API ist aktiviert")
        sys.exit(1)


def main():
    """CLI Hauptfunktion"""
    parser = argparse.ArgumentParser(
        description="Docassemble MCP Server - Stellt alle 61 Docassemble API Endpunkte für LLMs zur Verfügung",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  mcp-docassemble serve
  mcp-docassemble test-connection --base-url https://demo.docassemble.org --api-key your_key
  
Umgebungsvariablen:
  DOCASSEMBLE_BASE_URL    Base URL der Docassemble Installation
  DOCASSEMBLE_API_KEY     API Key für Authentifizierung
        """,
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Ausführliche Ausgabe aktivieren"
    )

    subparsers = parser.add_subparsers(dest="command", help="Verfügbare Befehle")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Startet den MCP Server")
    serve_parser.set_defaults(func=serve_command)

    # Test command
    test_parser = subparsers.add_parser(
        "test-connection", help="Testet die Verbindung zur Docassemble API"
    )
    test_parser.add_argument(
        "--base-url", help="Docassemble Base URL (überschreibt Umgebungsvariable)"
    )
    test_parser.add_argument(
        "--api-key", help="API Key (überschreibt Umgebungsvariable)"
    )
    test_parser.set_defaults(func=test_command)

    args = parser.parse_args()

    # Setup logging based on verbosity
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        setup_logging()

    # Default to serve if no command given
    if not args.command:
        args.command = "serve"
        args.func = serve_command

    # Execute command
    if args.command == "serve":
        validate_environment()
        asyncio.run(args.func(args))
    else:
        args.func(args)


if __name__ == "__main__":
    main()

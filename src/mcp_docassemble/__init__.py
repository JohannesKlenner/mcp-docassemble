"""
Docassemble Model Context Protocol (MCP) Server

Ein umfassender MCP Server für die Integration mit Docassemble APIs.
Stellt alle 61 Docassemble API Endpunkte als Tools für Large Language Models zur Verfügung.

Kategorien der verfügbaren API Endpunkte:
- Benutzer-Management (9 Endpunkte): Erstellen, Bearbeiten, Verwalten von Benutzern
- Berechtigungen (4 Endpunkte): Benutzerrechte verwalten  
- Interview Sessions (10 Endpunkte): Sessions auflisten, löschen, verwalten
- Interview Operations (8 Endpunkte): Interviews starten, Variablen setzen, Aktionen ausführen
- Playground (9 Endpunkte): Dateien und Projekte im Playground verwalten
- System Administration (8 Endpunkte): Packages installieren, Server konfigurieren
- API Key Management (6 Endpunkte): API Keys erstellen und verwalten
- File Operations (3 Endpunkte): Interview Dateien analysieren
- Data Stashing (2 Endpunkte): Temporäre Datenspeicherung

Verwendung:
    from mcp_docassemble import create_server
    
    server = create_server()
    # Konfiguration über Umgebungsvariablen:
    # DOCASSEMBLE_BASE_URL=https://docassemble.example.com
    # DOCASSEMBLE_API_KEY=your_api_key_here
    
    asyncio.run(server.run())
"""

__version__ = "0.1.0"
__author__ = "Docassemble MCP Development Team"

from .server import create_server, DocassembleServer
from .client import DocassembleClient, DocassembleAPIError

__all__ = [
    "create_server",
    "DocassembleServer", 
    "DocassembleClient",
    "DocassembleAPIError"
]

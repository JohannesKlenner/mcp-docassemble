"""
MCP Docassemble Server

Ein Model Context Protocol Server, der vollständigen Zugriff auf alle 61 Docassemble API Endpunkte bietet.
Jedes Tool ist ausführlich dokumentiert mit erforderlichen Parametern und Berechtigungen.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urlparse

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in project root
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logging.info(f"Loaded environment from {env_path}")
    else:
        # Also try current working directory
        load_dotenv()
except ImportError:
    # python-dotenv not installed - use environment variables only
    pass

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest, 
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    JSONRPCError
)
from pydantic import BaseModel

from .client import DocassembleClient, DocassembleAPIError


logger = logging.getLogger(__name__)


class DocassembleServer:
    """MCP Server für umfassende Docassemble API Integration"""
    
    def __init__(self):
        self.server = Server("docassemble-mcp")
        self.client: Optional[DocassembleClient] = None
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Registriert alle MCP Handler"""
        
        @self.server.list_tools()
        async def list_tools(request: ListToolsRequest) -> ListToolsResult:
            """Listet alle verfügbaren Docassemble API Tools"""
            
            tools = [
                # ====================================================================
                # BENUTZER-MANAGEMENT (9 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_create_user",
                    description="""Erstellt einen neuen Benutzer im Docassemble System.
                    
                    Erforderliche Berechtigungen: admin oder (access_user_info und create_user)
                    
                    Parameter:
                    - username (erforderlich): E-Mail Adresse des Benutzers
                    - password (optional): Passwort (wird automatisch generiert wenn nicht angegeben)
                    - privileges (optional): Liste der Benutzerrechte ['user', 'admin', 'developer', 'advocate']
                    - first_name (optional): Vorname
                    - last_name (optional): Nachname
                    - country (optional): Ländercode (z.B. 'US', 'DE')
                    - subdivisionfirst (optional): Bundesland/Staat
                    - subdivisionsecond (optional): Landkreis
                    - subdivisionthird (optional): Gemeinde
                    - organization (optional): Organisation
                    - timezone (optional): Zeitzone (z.B. 'Europe/Berlin', 'America/New_York')
                    - language (optional): Sprachcode (z.B. 'en', 'de')
                    
                    Rückgabe: Dict mit user_id und password des neuen Benutzers""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {"type": "string", "description": "E-Mail Adresse des Benutzers"},
                            "password": {"type": "string", "description": "Passwort (optional)"},
                            "privileges": {
                                "type": "array", 
                                "items": {"type": "string"},
                                "description": "Liste der Benutzerrechte"
                            },
                            "first_name": {"type": "string", "description": "Vorname"},
                            "last_name": {"type": "string", "description": "Nachname"},
                            "country": {"type": "string", "description": "Ländercode"},
                            "subdivisionfirst": {"type": "string", "description": "Bundesland/Staat"},
                            "subdivisionsecond": {"type": "string", "description": "Landkreis"},
                            "subdivisionthird": {"type": "string", "description": "Gemeinde"},
                            "organization": {"type": "string", "description": "Organisation"},
                            "timezone": {"type": "string", "description": "Zeitzone"},
                            "language": {"type": "string", "description": "Sprachcode"}
                        },
                        "required": ["username"]
                    }
                ),
                
                Tool(
                    name="docassemble_invite_users",
                    description="""Lädt neue Benutzer per E-Mail ins Docassemble System ein.
                    
                    Erforderliche Berechtigungen: admin oder create_user
                    
                    Parameter:
                    - email_addresses (erforderlich): Liste der E-Mail Adressen
                    - privileges (optional): Liste der Benutzerrechte für alle Eingeladenen
                    - send_emails (optional): Ob E-Mail Einladungen gesendet werden sollen (default: true)
                    
                    Rückgabe: Liste mit Einladungsdetails für jede E-Mail""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "email_addresses": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Liste der E-Mail Adressen"
                            },
                            "privileges": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Liste der Benutzerrechte"
                            },
                            "send_emails": {"type": "boolean", "description": "Ob E-Mails gesendet werden sollen"}
                        },
                        "required": ["email_addresses"]
                    }
                ),
                
                Tool(
                    name="docassemble_list_users",
                    description="""Listet alle registrierten Benutzer im System (paginiert).
                    
                    Erforderliche Berechtigungen: admin, advocate oder access_user_info
                    
                    Parameter:
                    - include_inactive (optional): Ob inaktive Benutzer eingeschlossen werden sollen
                    - next_id (optional): ID für nächste Seite der Ergebnisse (Pagination)
                    
                    Rückgabe: Dict mit 'items' (Benutzerliste) und 'next_id' für weitere Seiten""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_inactive": {"type": "boolean", "description": "Inaktive Benutzer einschließen"},
                            "next_id": {"type": "string", "description": "ID für nächste Seite"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_get_user_by_username",
                    description="""Holt Benutzerinformationen per Benutzername (E-Mail).
                    
                    Erforderliche Berechtigungen: admin, advocate oder access_user_info
                    
                    Parameter:
                    - username (erforderlich): Benutzername (E-Mail Adresse)
                    
                    Rückgabe: Vollständige Benutzerinformationen""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {"type": "string", "description": "Benutzername (E-Mail)"}
                        },
                        "required": ["username"]
                    }
                ),
                
                Tool(
                    name="docassemble_get_current_user",
                    description="""Holt Informationen über den aktuellen Benutzer (API Key Besitzer).
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Rückgabe: Benutzerinformationen des API Key Besitzers""",
                    inputSchema={"type": "object", "properties": {}}
                ),
                
                Tool(
                    name="docassemble_update_current_user",
                    description="""Aktualisiert Informationen des aktuellen Benutzers.
                    
                    Erforderliche Berechtigungen: edit_user_info für Profildaten, edit_user_password für Passwort
                    
                    Parameter (alle optional):
                    - first_name: Neuer Vorname
                    - last_name: Neuer Nachname  
                    - country: Neuer Ländercode
                    - subdivisionfirst: Neues Bundesland/Staat
                    - subdivisionsecond: Neuer Landkreis
                    - subdivisionthird: Neue Gemeinde
                    - organization: Neue Organisation
                    - timezone: Neue Zeitzone
                    - language: Neue Sprache
                    - password: Neues Passwort
                    - old_password: Altes Passwort (für Verschlüsselungskonvertierung)""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "country": {"type": "string"},
                            "subdivisionfirst": {"type": "string"},
                            "subdivisionsecond": {"type": "string"},
                            "subdivisionthird": {"type": "string"},
                            "organization": {"type": "string"},
                            "timezone": {"type": "string"},
                            "language": {"type": "string"},
                            "password": {"type": "string"},
                            "old_password": {"type": "string"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_get_user_by_id",
                    description="""Holt Informationen über einen Benutzer per ID.
                    
                    Erforderliche Berechtigungen: admin, advocate, eigene ID oder access_user_info
                    
                    Parameter:
                    - user_id (erforderlich): Benutzer ID
                    
                    Rückgabe: Vollständige Benutzerinformationen""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "Benutzer ID"}
                        },
                        "required": ["user_id"]
                    }
                ),
                
                Tool(
                    name="docassemble_deactivate_user",
                    description="""Deaktiviert oder löscht einen Benutzer.
                    
                    Erforderliche Berechtigungen: admin oder entsprechende Permissions
                    
                    Parameter:
                    - user_id (erforderlich): Benutzer ID
                    - remove (optional): 'account' zum Löschen, 'account_and_shared' für vollständiges Löschen""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "Benutzer ID"},
                            "remove": {"type": "string", "enum": ["account", "account_and_shared"]}
                        },
                        "required": ["user_id"]
                    }
                ),
                
                Tool(
                    name="docassemble_update_user",
                    description="""Aktualisiert Informationen eines Benutzers.
                    
                    Erforderliche Berechtigungen: admin oder entsprechende Permissions
                    
                    Parameter:
                    - user_id (erforderlich): Benutzer ID
                    - Alle weiteren Parameter optional wie bei update_current_user
                    - active (optional): Aktiv-Status des Benutzers""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "Benutzer ID"},
                            "country": {"type": "string"},
                            "first_name": {"type": "string"},
                            "language": {"type": "string"},
                            "last_name": {"type": "string"},
                            "organization": {"type": "string"},
                            "subdivisionfirst": {"type": "string"},
                            "subdivisionsecond": {"type": "string"},
                            "subdivisionthird": {"type": "string"},
                            "timezone": {"type": "string"},
                            "password": {"type": "string"},
                            "old_password": {"type": "string"},
                            "active": {"type": "boolean"}
                        },
                        "required": ["user_id"]
                    }
                ),

                # ====================================================================
                # BERECHTIGUNGEN (4 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_list_privileges",
                    description="""Listet alle verfügbaren Berechtigungen im System.
                    
                    Erforderliche Berechtigungen: admin, developer oder access_privileges
                    
                    Rückgabe: Liste der verfügbaren Berechtigungsnamen""",
                    inputSchema={"type": "object", "properties": {}}
                ),
                
                Tool(
                    name="docassemble_give_user_privilege",
                    description="""Gibt einem Benutzer eine Berechtigung.
                    
                    Erforderliche Berechtigungen: admin oder (access_privileges und edit_user_privileges)
                    
                    Parameter:
                    - user_id (erforderlich): Benutzer ID
                    - privilege (erforderlich): Name der Berechtigung""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "Benutzer ID"},
                            "privilege": {"type": "string", "description": "Berechtigung"}
                        },
                        "required": ["user_id", "privilege"]
                    }
                ),
                
                Tool(
                    name="docassemble_remove_user_privilege",
                    description="""Entzieht einem Benutzer eine Berechtigung.
                    
                    Erforderliche Berechtigungen: admin oder edit_user_privileges
                    
                    Parameter:
                    - user_id (erforderlich): Benutzer ID
                    - privilege (erforderlich): Name der Berechtigung""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer", "description": "Benutzer ID"},
                            "privilege": {"type": "string", "description": "Berechtigung"}
                        },
                        "required": ["user_id", "privilege"]
                    }
                ),

                # ====================================================================
                # INTERVIEW SESSIONS (10 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_list_interview_sessions",
                    description="""Listet Interview Sessions im System (paginiert).
                    
                    Erforderliche Berechtigungen: admin, advocate oder access_sessions
                    
                    Parameter (alle optional):
                    - secret: Entschlüsselungskey für verschlüsselte Sessions
                    - i: Interview Dateiname Filter (z.B. 'docassemble.demo:data/questions/questions.yml')
                    - session: Session ID Filter
                    - query: Session Query String Filter
                    - tag: Tag Filter
                    - include_dictionary: Ob Interview Antworten eingeschlossen werden sollen
                    - next_id: ID für nächste Seite
                    
                    Rückgabe: Dict mit 'items' (Session Liste) und 'next_id'""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "secret": {"type": "string"},
                            "i": {"type": "string", "description": "Interview Dateiname"},
                            "session": {"type": "string", "description": "Session ID"},
                            "query": {"type": "string", "description": "Query String"},
                            "tag": {"type": "string"},
                            "include_dictionary": {"type": "boolean"},
                            "next_id": {"type": "string"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_delete_interview_sessions",
                    description="""Löscht Interview Sessions im System.
                    
                    Erforderliche Berechtigungen: admin oder (access_sessions und edit_sessions)
                    
                    Parameter (alle optional als Filter):
                    - i: Interview Dateiname Filter
                    - session: Session ID Filter
                    - query: Session Query String Filter
                    - tag: Tag Filter
                    
                    WARNUNG: Ohne Filter werden ALLE Sessions gelöscht!""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string"},
                            "session": {"type": "string"},
                            "query": {"type": "string"},
                            "tag": {"type": "string"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_list_advertised_interviews",
                    description="""Holt Liste der beworbenen/verfügbaren Interviews.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter (optional):
                    - tag: Tag Filter für Interviews
                    - absolute_urls: Ob absolute URLs zurückgegeben werden sollen (default: true)
                    
                    Rückgabe: Liste der verfügbaren Interviews mit Metadaten""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tag": {"type": "string"},
                            "absolute_urls": {"type": "boolean"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_get_user_secret",
                    description="""Holt Entschlüsselungskey für einen Benutzer.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - username (erforderlich): Benutzername
                    - password (erforderlich): Passwort
                    
                    Rückgabe: Entschlüsselungskey als String""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "password": {"type": "string"}
                        },
                        "required": ["username", "password"]
                    }
                ),
                
                Tool(
                    name="docassemble_get_login_url",
                    description="""Erstellt temporäre Login URL für einen Benutzer.
                    
                    Erforderliche Berechtigungen: admin oder log_user_in
                    
                    Parameter:
                    - username (erforderlich): Benutzername
                    - password (erforderlich): Passwort
                    - i (optional): Interview Dateiname
                    - session (optional): Session ID
                    - resume_existing (optional): Existierende Session fortsetzen
                    - expire (optional): Ablaufzeit in Sekunden (default: 15)
                    - url_args (optional): Zusätzliche URL Parameter (JSON Objekt)
                    - next_page (optional): Seite nach Login (statt Interview)
                    
                    Rückgabe: Temporäre Login URL""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                            "i": {"type": "string"},
                            "session": {"type": "string"},
                            "resume_existing": {"type": "boolean"},
                            "expire": {"type": "integer"},
                            "url_args": {"type": "object"},
                            "next_page": {"type": "string"}
                        },
                        "required": ["username", "password"]
                    }
                ),

                # ====================================================================
                # INTERVIEW OPERATIONS (8 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_start_interview",
                    description="""Startet eine neue Interview Session.
                    
                    Erforderliche Berechtigungen: Keine (abhängig vom Interview)
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname (z.B. 'docassemble.demo:data/questions/questions.yml')
                    - secret (optional): Verschlüsselungskey
                    - Alle weiteren Parameter werden als url_args übergeben
                    
                    Rückgabe: Dict mit session ID, encrypted Status und optional secret""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string", "description": "Interview Dateiname"},
                            "secret": {"type": "string", "description": "Verschlüsselungskey"}
                        },
                        "required": ["i"],
                        "additionalProperties": True
                    }
                ),
                
                Tool(
                    name="docassemble_get_interview_variables",
                    description="""Holt alle Variablen aus einer Interview Session.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname
                    - session (erforderlich): Session ID
                    - secret (optional): Entschlüsselungskey (falls verschlüsselt)
                    
                    Rückgabe: JSON Repräsentation des Interview Dictionary""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string"},
                            "session": {"type": "string"},
                            "secret": {"type": "string"}
                        },
                        "required": ["i", "session"]
                    }
                ),
                
                Tool(
                    name="docassemble_set_interview_variables",
                    description="""Setzt Variablen in einer Interview Session.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname
                    - session (erforderlich): Session ID
                    - secret (optional): Entschlüsselungskey
                    - variables (optional): Dict mit Variablen und Werten
                    - raw (optional): Datum/Objekt Konvertierung überspringen
                    - question_name (optional): Name der beantworteten Frage
                    - question (optional): Interview nach Setzen evaluieren (default: true)
                    - delete_variables (optional): Liste zu löschender Variablen
                    
                    Rückgabe: JSON der aktuellen Frage oder None wenn question=false""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string"},
                            "session": {"type": "string"},
                            "secret": {"type": "string"},
                            "variables": {"type": "object"},
                            "raw": {"type": "boolean"},
                            "question_name": {"type": "string"},
                            "question": {"type": "boolean"},
                            "delete_variables": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["i", "session"]
                    }
                ),
                
                Tool(
                    name="docassemble_get_current_question",
                    description="""Holt Informationen über die aktuelle Frage in einem Interview.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname
                    - session (erforderlich): Session ID
                    - secret (optional): Entschlüsselungskey
                    
                    Rückgabe: JSON Repräsentation der aktuellen Frage""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string"},
                            "session": {"type": "string"},
                            "secret": {"type": "string"}
                        },
                        "required": ["i", "session"]
                    }
                ),
                
                Tool(
                    name="docassemble_run_interview_action",
                    description="""Führt eine Aktion in einem Interview aus.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname
                    - session (erforderlich): Session ID
                    - action (erforderlich): Name der auszuführenden Aktion
                    - secret (optional): Entschlüsselungskey
                    - persistent (optional): Ob Aktion eine Frage zeigen soll
                    - arguments (optional): Argumente für die Aktion (JSON Objekt)
                    - overwrite (optional): Vorherige Antworten überschreiben
                    - read_only (optional): Antworten nicht speichern
                    
                    Rückgabe: Response Content oder None""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string"},
                            "session": {"type": "string"},
                            "action": {"type": "string"},
                            "secret": {"type": "string"},
                            "persistent": {"type": "boolean"},
                            "arguments": {"type": "object"},
                            "overwrite": {"type": "boolean"},
                            "read_only": {"type": "boolean"}
                        },
                        "required": ["i", "session", "action"]
                    }
                ),
                
                Tool(
                    name="docassemble_go_back_in_interview",
                    description="""Geht einen Schritt zurück in der Interview Session.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname
                    - session (erforderlich): Session ID
                    - secret (optional): Entschlüsselungskey
                    - question (optional): Aktuelle Frage zurückgeben (default: true)
                    
                    Rückgabe: JSON der aktuellen Frage oder None""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string"},
                            "session": {"type": "string"},
                            "secret": {"type": "string"},
                            "question": {"type": "boolean"}
                        },
                        "required": ["i", "session"]
                    }
                ),
                
                Tool(
                    name="docassemble_delete_interview_session",
                    description="""Löscht eine spezifische Interview Session.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname
                    - session (erforderlich): Session ID""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string"},
                            "session": {"type": "string"}
                        },
                        "required": ["i", "session"]
                    }
                ),

                # ====================================================================
                # PLAYGROUND (9 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_list_playground_files",
                    description="""Listet Dateien im Playground oder lädt eine spezifische Datei.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control
                    
                    Parameter:
                    - user_id (optional): Benutzer ID (nur admins können andere zugreifen)
                    - folder (optional): Ordner ('questions', 'sources', 'static', 'templates', 'modules', 'packages')
                    - project (optional): Projekt Name (default: 'default')
                    - filename (optional): Dateiname zum Download
                    
                    Rückgabe: Liste der Dateien oder Dateiinhalt""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"},
                            "folder": {"type": "string", "enum": ["questions", "sources", "static", "templates", "modules", "packages"]},
                            "project": {"type": "string"},
                            "filename": {"type": "string"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_delete_playground_file",
                    description="""Löscht eine Datei aus dem Playground.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control
                    
                    Parameter:
                    - filename (erforderlich): Dateiname zum Löschen
                    - user_id (optional): Benutzer ID
                    - folder (optional): Ordner Name (default: 'static')
                    - project (optional): Projekt Name (default: 'default')
                    
                    Rückgabe: Task ID für Restart wenn nötig""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filename": {"type": "string"},
                            "user_id": {"type": "integer"},
                            "folder": {"type": "string"},
                            "project": {"type": "string"}
                        },
                        "required": ["filename"]
                    }
                ),
                
                Tool(
                    name="docassemble_list_playground_projects",
                    description="""Listet Projekte im Playground.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control
                    
                    Parameter:
                    - user_id (optional): Benutzer ID
                    
                    Rückgabe: Liste der Projekt Namen""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_create_playground_project",
                    description="""Erstellt ein neues Projekt im Playground.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control
                    
                    Parameter:
                    - project (erforderlich): Projekt Name
                    - user_id (optional): Benutzer ID""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {"type": "string"},
                            "user_id": {"type": "integer"}
                        },
                        "required": ["project"]
                    }
                ),
                
                Tool(
                    name="docassemble_delete_playground_project",
                    description="""Löscht ein Projekt aus dem Playground.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control
                    
                    Parameter:
                    - project (erforderlich): Projekt Name
                    - user_id (optional): Benutzer ID""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {"type": "string"},
                            "user_id": {"type": "integer"}
                        },
                        "required": ["project"]
                    }
                ),
                
                Tool(
                    name="docassemble_clear_interview_cache",
                    description="""Löscht den Interview Cache, damit YAML neu gelesen wird.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control""",
                    inputSchema={"type": "object", "properties": {}}
                ),

                # ====================================================================
                # SYSTEM ADMINISTRATION (8 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_get_server_config",
                    description="""Holt die Server Konfiguration.
                    
                    Erforderliche Berechtigungen: admin
                    
                    Rückgabe: Server Konfiguration als JSON""",
                    inputSchema={"type": "object", "properties": {}}
                ),
                
                Tool(
                    name="docassemble_list_installed_packages",
                    description="""Listet installierte Python Packages.
                    
                    Erforderliche Berechtigungen: admin oder developer
                    
                    Rückgabe: Liste der installierten Packages mit Details""",
                    inputSchema={"type": "object", "properties": {}}
                ),
                
                Tool(
                    name="docassemble_install_package",
                    description="""Installiert oder aktualisiert ein Package.
                    
                    Erforderliche Berechtigungen: admin oder developer
                    
                    Parameter (einer erforderlich):
                    - update: Package Name zum Aktualisieren
                    - github_url: GitHub URL für Installation
                    - pip: PyPI Package Name
                    - branch (optional): Git Branch
                    - restart (optional): Server restart (default: true)
                    
                    Rückgabe: Task ID für Monitoring""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "update": {"type": "string"},
                            "github_url": {"type": "string"},
                            "pip": {"type": "string"},
                            "branch": {"type": "string"},
                            "restart": {"type": "boolean"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_uninstall_package",
                    description="""Deinstalliert ein Package.
                    
                    Erforderliche Berechtigungen: admin oder developer
                    
                    Parameter:
                    - package (erforderlich): Package Name
                    - restart (optional): Server restart (default: true)
                    
                    Rückgabe: Task ID für Monitoring""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "package": {"type": "string"},
                            "restart": {"type": "boolean"}
                        },
                        "required": ["package"]
                    }
                ),
                
                Tool(
                    name="docassemble_get_package_update_status",
                    description="""Überprüft Status eines Package Update Prozesses.
                    
                    Erforderliche Berechtigungen: admin oder developer
                    
                    Parameter:
                    - task_id (erforderlich): Task ID vom Package Update
                    
                    Rückgabe: Status Information""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"}
                        },
                        "required": ["task_id"]
                    }
                ),
                
                Tool(
                    name="docassemble_trigger_server_restart",
                    description="""Löst einen Server Restart aus.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control
                    
                    Rückgabe: Task ID für Restart Monitoring""",
                    inputSchema={"type": "object", "properties": {}}
                ),
                
                Tool(
                    name="docassemble_get_restart_status",
                    description="""Überprüft Status eines Server Restarts.
                    
                    Erforderliche Berechtigungen: admin, developer oder playground_control
                    
                    Parameter:
                    - task_id (erforderlich): Task ID vom Restart
                    
                    Rückgabe: Status Information""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"}
                        },
                        "required": ["task_id"]
                    }
                ),

                # ====================================================================
                # API KEY MANAGEMENT (6 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_get_user_api_keys",
                    description="""Holt API Key Informationen des aktuellen Benutzers.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter (optional):
                    - api_key: Spezifischer API Key
                    - name: API Key Name
                    
                    Rückgabe: API Key Details oder Liste aller API Keys""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "api_key": {"type": "string"},
                            "name": {"type": "string"}
                        }
                    }
                ),
                
                Tool(
                    name="docassemble_create_user_api_key",
                    description="""Erstellt einen neuen API Key für den aktuellen Benutzer.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - name (erforderlich): Name des API Keys
                    - method (optional): Zugriffsmethode ('ip', 'referer', 'none')
                    - allowed (optional): Liste erlaubter IPs oder URLs
                    - permissions (optional): Beschränkte Berechtigungen (nur für admins)
                    
                    Rückgabe: Neuer API Key""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "method": {"type": "string", "enum": ["ip", "referer", "none"]},
                            "allowed": {"type": "array", "items": {"type": "string"}},
                            "permissions": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["name"]
                    }
                ),
                
                Tool(
                    name="docassemble_delete_user_api_key",
                    description="""Löscht einen API Key des aktuellen Benutzers.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - api_key (erforderlich): API Key zum Löschen""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "api_key": {"type": "string"}
                        },
                        "required": ["api_key"]
                    }
                ),

                # ====================================================================
                # FILE OPERATIONS (3 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_get_interview_data",
                    description="""Holt Informationen über ein Interview (Python Namen, Variablen, etc.).
                    
                    Erforderliche Berechtigungen: admin, developer oder interview_data
                    
                    Parameter:
                    - i (erforderlich): Interview Dateiname
                    
                    Rückgabe: Interview Datenanalyse mit Variablen, Modulen, etc.""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "i": {"type": "string", "description": "Interview Dateiname"}
                        },
                        "required": ["i"]
                    }
                ),

                # ====================================================================
                # DATA STASHING (2 Tools)
                # ====================================================================
                Tool(
                    name="docassemble_stash_data",
                    description="""Speichert Daten temporär verschlüsselt.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - data (erforderlich): Zu speichernde Daten (JSON Objekt)
                    - expire (optional): Ablaufzeit in Sekunden (default: 90 Tage)
                    - raw (optional): Datum/Objekt Konvertierung überspringen
                    
                    Rückgabe: Dict mit stash_key und secret""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data": {"type": "object"},
                            "expire": {"type": "integer"},
                            "raw": {"type": "boolean"}
                        },
                        "required": ["data"]
                    }
                ),
                
                Tool(
                    name="docassemble_retrieve_stashed_data",
                    description="""Holt temporär gespeicherte Daten.
                    
                    Erforderliche Berechtigungen: Keine
                    
                    Parameter:
                    - stash_key (erforderlich): Stash Schlüssel
                    - secret (erforderlich): Entschlüsselungsgeheimnis
                    - delete (optional): Daten nach Abruf löschen
                    - refresh (optional): Neue Ablaufzeit in Sekunden
                    
                    Rückgabe: Gespeicherte Daten""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "stash_key": {"type": "string"},
                            "secret": {"type": "string"},
                            "delete": {"type": "boolean"},
                            "refresh": {"type": "integer"}
                        },
                        "required": ["stash_key", "secret"]
                    }
                )
            ]
            
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def call_tool(request: CallToolRequest) -> CallToolResult:
            """Führt Docassemble API Aufrufe aus"""
            
            if not self.client:
                raise JSONRPCError(
                    code=-1,
                    message="Docassemble Client nicht initialisiert. Base URL und API Key erforderlich."
                )
            
            try:
                result = await self._execute_tool(request.params.name, request.params.arguments or {})
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=json.dumps(result, indent=2, ensure_ascii=False)
                        )
                    ]
                )
                
            except DocassembleAPIError as e:
                error_msg = f"Docassemble API Fehler: {str(e)}"
                if e.status_code:
                    error_msg += f" (Status: {e.status_code})"
                if e.response_data:
                    error_msg += f"\nResponse: {e.response_data}"
                    
                raise JSONRPCError(code=-1, message=error_msg)
                
            except Exception as e:
                raise JSONRPCError(
                    code=-1,
                    message=f"Unerwarteter Fehler bei {request.params.name}: {str(e)}"
                )
    
    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Führt das angegebene Tool aus"""
        
        # Map tool names to client methods
        tool_mapping = {
            # Benutzer-Management
            "docassemble_create_user": "create_user",
            "docassemble_invite_users": "invite_users", 
            "docassemble_list_users": "list_users",
            "docassemble_get_user_by_username": "get_user_by_username",
            "docassemble_get_current_user": "get_current_user",
            "docassemble_update_current_user": "update_current_user",
            "docassemble_get_user_by_id": "get_user_by_id",
            "docassemble_deactivate_user": "deactivate_user",
            "docassemble_update_user": "update_user",
            
            # Berechtigungen
            "docassemble_list_privileges": "list_privileges",
            "docassemble_give_user_privilege": "give_user_privilege",
            "docassemble_remove_user_privilege": "remove_user_privilege",
            
            # Interview Sessions
            "docassemble_list_interview_sessions": "list_interview_sessions",
            "docassemble_delete_interview_sessions": "delete_interview_sessions",
            "docassemble_list_advertised_interviews": "list_advertised_interviews",
            "docassemble_get_user_secret": "get_user_secret",
            "docassemble_get_login_url": "get_login_url",
            
            # Interview Operations
            "docassemble_start_interview": "start_interview",
            "docassemble_get_interview_variables": "get_interview_variables",
            "docassemble_set_interview_variables": "set_interview_variables",
            "docassemble_get_current_question": "get_current_question",
            "docassemble_run_interview_action": "run_interview_action",
            "docassemble_go_back_in_interview": "go_back_in_interview",
            "docassemble_delete_interview_session": "delete_interview_session",
            
            # Playground
            "docassemble_list_playground_files": "list_playground_files",
            "docassemble_delete_playground_file": "delete_playground_file",
            "docassemble_list_playground_projects": "list_playground_projects",
            "docassemble_create_playground_project": "create_playground_project",
            "docassemble_delete_playground_project": "delete_playground_project",
            "docassemble_clear_interview_cache": "clear_interview_cache",
            
            # System Administration
            "docassemble_get_server_config": "get_server_config",
            "docassemble_list_installed_packages": "list_installed_packages",
            "docassemble_install_package": "install_or_update_package",
            "docassemble_uninstall_package": "uninstall_package",
            "docassemble_get_package_update_status": "get_package_update_status",
            "docassemble_trigger_server_restart": "trigger_server_restart",
            "docassemble_get_restart_status": "get_restart_status",
            
            # API Key Management
            "docassemble_get_user_api_keys": "get_user_api_keys",
            "docassemble_create_user_api_key": "create_user_api_key",
            "docassemble_delete_user_api_key": "delete_user_api_key",
            
            # File Operations
            "docassemble_get_interview_data": "get_interview_data",
            
            # Data Stashing
            "docassemble_stash_data": "stash_data",
            "docassemble_retrieve_stashed_data": "retrieve_stashed_data"
        }
        
        method_name = tool_mapping.get(tool_name)
        if not method_name:
            raise ValueError(f"Unbekanntes Tool: {tool_name}")
        
        method = getattr(self.client, method_name)
        
        # Special handling for start_interview which accepts **kwargs
        if tool_name == "docassemble_start_interview":
            i = arguments.pop('i')
            secret = arguments.pop('secret', None)
            # Pass remaining arguments as url_args
            return method(i=i, secret=secret, **arguments)
        
        return method(**arguments)
    
    def setup_client(self, base_url: str, api_key: str):
        """Konfiguriert den Docassemble Client"""
        self.client = DocassembleClient(base_url, api_key)
    
    async def run(self):
        """Startet den MCP Server"""
        # Check for required environment variables
        base_url = os.getenv('DOCASSEMBLE_BASE_URL')
        api_key = os.getenv('DOCASSEMBLE_API_KEY')
        
        if not base_url or not api_key:
            logger.error("DOCASSEMBLE_BASE_URL und DOCASSEMBLE_API_KEY Umgebungsvariablen sind erforderlich")
            raise ValueError("Docassemble Konfiguration fehlt")
        
        # Setup client
        self.setup_client(base_url, api_key)
        
        # Start server
        logger.info(f"Starte Docassemble MCP Server für {base_url}")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="docassemble-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )


def create_server() -> DocassembleServer:
    """Factory Funktion zum Erstellen eines Docassemble MCP Servers"""
    return DocassembleServer()


if __name__ == "__main__":
    server = create_server()
    asyncio.run(server.run())

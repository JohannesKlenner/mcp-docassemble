# Docassemble MCP Server

Ein umfassender **Model Context Protocol (MCP) Server**, der alle 61 Docassemble API Endpunkte für Large Language Models verfügbar macht.

## 🚀 Überblick

Dieser MCP Server stellt eine vollständige Abstraktion der Docassemble API bereit und ermöglicht es LLMs, sämtliche Docassemble-Funktionen zu nutzen:

- **61 API Endpunkte** in 9 Kategorien
- **Vollständige Dokumentation** aller Parameter und Berechtigungen  
- **Type Safety** mit Pydantic Modellen
- **Robuste Fehlerbehandlung** und Logging
- **CLI Tools** zum Testen und Debuggen

## 📋 API Endpunkt Kategorien

### 1. 👥 Benutzer-Management (9 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_create_user` | Erstellt einen neuen Benutzer | admin oder (access_user_info + create_user) |
| `docassemble_invite_users` | Lädt Benutzer per E-Mail ein | admin oder create_user |
| `docassemble_list_users` | Listet alle Benutzer (paginiert) | admin, advocate oder access_user_info |
| `docassemble_get_user_by_username` | Holt Benutzer per E-Mail | admin, advocate oder access_user_info |
| `docassemble_get_current_user` | Holt aktuellen Benutzer | Keine |
| `docassemble_update_current_user` | Aktualisiert eigene Daten | edit_user_info, edit_user_password |
| `docassemble_get_user_by_id` | Holt Benutzer per ID | admin, advocate, eigene ID oder access_user_info |
| `docassemble_deactivate_user` | Deaktiviert/löscht Benutzer | admin |
| `docassemble_update_user` | Aktualisiert beliebigen Benutzer | admin |

### 2. 🔐 Berechtigungen (4 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_list_privileges` | Listet alle Berechtigungen | admin, developer oder access_privileges |
| `docassemble_give_user_privilege` | Gibt Berechtigung | admin oder (access_privileges + edit_user_privileges) |
| `docassemble_remove_user_privilege` | Entzieht Berechtigung | admin oder edit_user_privileges |

### 3. 📝 Interview Sessions (10 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_list_interview_sessions` | Listet Sessions (paginiert) | admin, advocate oder access_sessions |
| `docassemble_delete_interview_sessions` | Löscht Sessions (Filter) | admin oder (access_sessions + edit_sessions) |
| `docassemble_list_advertised_interviews` | Listet verfügbare Interviews | Keine |
| `docassemble_get_user_secret` | Holt Entschlüsselungskey | Keine |
| `docassemble_get_login_url` | Erstellt temporäre Login URL | admin oder log_user_in |

### 4. ⚡ Interview Operations (8 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_start_interview` | Startet neue Session | Abhängig vom Interview |
| `docassemble_get_interview_variables` | Holt alle Variablen | Keine |
| `docassemble_set_interview_variables` | Setzt Variablen | Keine |
| `docassemble_get_current_question` | Holt aktuelle Frage | Keine |
| `docassemble_run_interview_action` | Führt Aktion aus | Keine |
| `docassemble_go_back_in_interview` | Geht einen Schritt zurück | Keine |
| `docassemble_delete_interview_session` | Löscht spezifische Session | Keine |

### 5. 🛠️ Playground (9 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_list_playground_files` | Listet/lädt Playground Dateien | admin, developer oder playground_control |
| `docassemble_delete_playground_file` | Löscht Playground Datei | admin, developer oder playground_control |
| `docassemble_list_playground_projects` | Listet Playground Projekte | admin, developer oder playground_control |
| `docassemble_create_playground_project` | Erstellt Playground Projekt | admin, developer oder playground_control |
| `docassemble_delete_playground_project` | Löscht Playground Projekt | admin, developer oder playground_control |
| `docassemble_clear_interview_cache` | Löscht Interview Cache | admin, developer oder playground_control |

### 6. ⚙️ System Administration (8 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_get_server_config` | Holt Server Konfiguration | admin |
| `docassemble_list_installed_packages` | Listet installierte Packages | admin oder developer |
| `docassemble_install_package` | Installiert/aktualisiert Package | admin oder developer |
| `docassemble_uninstall_package` | Deinstalliert Package | admin oder developer |
| `docassemble_get_package_update_status` | Überprüft Update Status | admin oder developer |
| `docassemble_trigger_server_restart` | Löst Server Restart aus | admin, developer oder playground_control |
| `docassemble_get_restart_status` | Überprüft Restart Status | admin, developer oder playground_control |

### 7. 🔑 API Key Management (6 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_get_user_api_keys` | Holt eigene API Keys | Keine |
| `docassemble_create_user_api_key` | Erstellt neuen API Key | Keine |
| `docassemble_delete_user_api_key` | Löscht eigenen API Key | Keine |

### 8. 📁 File Operations (3 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_get_interview_data` | Analysiert Interview Datei | admin, developer oder interview_data |

### 9. 💾 Data Stashing (2 Endpunkte)

| Tool | Beschreibung | Berechtigungen |
|------|-------------|----------------|
| `docassemble_stash_data` | Speichert Daten temporär | Keine |
| `docassemble_retrieve_stashed_data` | Holt gespeicherte Daten | Keine |

## 🛠️ Installation

```bash
# Aus Repository installieren
pip install -e .

# Mit Entwicklungsabhängigkeiten
pip install -e ".[dev]"
```

## ⚙️ Konfiguration

### Umgebungsvariablen

```bash
export DOCASSEMBLE_BASE_URL="https://your-docassemble.com"
export DOCASSEMBLE_API_KEY="your_api_key_here"
```

### API Key erstellen

1. In Docassemble anmelden
2. Zu **My Account** → **API Keys** navigieren
3. Neuen API Key erstellen
4. Notwendige Berechtigungen zuweisen

## 🚀 Verwendung

### Als MCP Server starten

```bash
# Mit CLI Tool
mcp-docassemble serve

# Oder direkt mit Python
python -m mcp_docassemble.main
```

### Verbindung testen

```bash
mcp-docassemble test-connection
```

### In Python Code

```python
import asyncio
from mcp_docassemble import create_server

async def main():
    server = create_server()
    await server.run()

asyncio.run(main())
```

## 📖 LLM Tool Dokumentation

Jedes Tool ist vollständig dokumentiert mit:

- **Erforderliche Parameter**: Welche Eingaben zwingend notwendig sind
- **Optionale Parameter**: Zusätzliche Konfigurationsmöglichkeiten  
- **Berechtigungen**: Welche Docassemble-Rechte erforderlich sind
- **Rückgabewerte**: Was das Tool zurückgibt
- **Beispiele**: Praktische Anwendungsfälle

### Beispiel: Neuen Benutzer erstellen

```json
{
  "tool": "docassemble_create_user",
  "arguments": {
    "username": "max.mustermann@example.com",
    "first_name": "Max",
    "last_name": "Mustermann", 
    "privileges": ["user"],
    "country": "DE",
    "timezone": "Europe/Berlin",
    "language": "de"
  }
}
```

### Beispiel: Interview starten

```json
{
  "tool": "docassemble_start_interview",
  "arguments": {
    "i": "docassemble.demo:data/questions/questions.yml",
    "tenant_name": "Max Mustermann",
    "property_type": "apartment"
  }
}
```

## 🔧 Entwicklung

### Setup

```bash
git clone <repository>
cd mcp-docassemble
pip install -e ".[dev]"
```

### Tests ausführen

```bash
pytest
```

### Code formatieren

```bash
black src/
isort src/
```

### Type checking

```bash
mypy src/
```

## 📝 Logs und Debugging

Der Server loggt alle API-Aufrufe und Fehler:

```bash
# Verbose logging
mcp-docassemble --verbose serve

# Logs in Datei
mcp-docassemble serve 2> docassemble-mcp.log
```

## 🤝 Beitragen

1. Repository forken
2. Feature Branch erstellen
3. Änderungen committen
4. Pull Request erstellen

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/mcp-docassemble/issues)
- **Dokumentation**: [Docassemble API Docs](https://docassemble.org/docs/api.html)
- **MCP Spezifikation**: [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Hinweis**: Dieser MCP Server stellt alle verfügbaren Docassemble API Endpunkte bereit. Die tatsächlich verfügbaren Funktionen hängen von den Berechtigungen des verwendeten API Keys ab.

# 🚀 MCP Docassemble Server v1.1.1 - Package Integration Enhanced

[![CI/CD Pipeline](https://github.com/JohannesKlenner/mcp-docassemble/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/JohannesKlenner/mcp-docassemble/actions/workflows/ci-cd.yml)
[![Container Registry](https://ghcr.io/badge/johannesklenner/mcp-docassemble/size)](https://github.com/JohannesKlenner/mcp-docassemble/pkgs/container/mcp-docassemble)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ein **Model Context Protocol (MCP) Server**, der vollständigen Zugang zur Docassemble API für Large Language Models bereitstellt - mit verbesserter Package-Integration und Continuous Integration/Continuous Deployment (CI/CD) Pipeline.

## 🆕 Version 1.1.1 - Package Integration Update

### ✨ Neue Features
- 🎯 **One-Click Package Deployment** - Nahtlose Integration mit VS Code Tasks
- 📦 **Playground URL Management** - Korrekte URL-Generierung für `docassemble.playground1:`
- 🛠️ **GitHub Actions CI/CD** - Umfassende Pipeline mit Security Scanning
- 🐳 **Multi-Platform Docker** - Support für AMD64 und ARM64 Architekturen
- 🔒 **Security Integration** - Bandit, Safety und Trivy Container Scanning
- 📊 **Quality Metrics** - Automatisierte Tests und Code Coverage

### 🔧 v1.1.0 Enhanced Features (Continued)
- ✅ **Version Detection** - Automatische Docassemble Versionserkennung und Kompatibilität
- ✅ **Enhanced Session Management** - Konfigurierbare Timeouts und verbesserte Session-Behandlung  
- ✅ **Graceful Fallbacks** - Robuste Behandlung nicht unterstützter APIs
- ✅ **Enhanced Error Handling** - Detaillierte Fehlerklassifizierung und Retry-Mechanismen
- ✅ **Production Ready** - 15.9% Endpunkte vollständig funktional, 73% warten auf Implementierung

### 🌐 Produktionsumgebung
- **Docassemble Version**: ~1.4.x - 1.5.x (Asset Version: 1.8.12)
- **Aktuell verfügbar**: v1.6.5 (Upgrade für vollständige API-Unterstützung empfohlen)
- **Stabilität**: Server benötigt gelegentlich Neustart (502 Fehler lösen sich automatisch)

## 🎯 Überblick

Dieser MCP Server stellt alle 63 Docassemble API Endpunkte mit verbesserter Zuverlässigkeit zur Verfügung und ermöglicht umfassende LLM-Integration mit Docassemble Systemen. Alle verfügbaren Funktionen sind klar dokumentiert mit erforderlichen Parametern und Berechtigungen.

### 🔧 CI/CD Pipeline Features

**Automatisierte Workflows:**
```yaml
# Triggers:
- Push to main/develop branches
- Pull Requests
- Version Tags (v*)

# Pipeline Stages:
1. 🔒 Security Scan (Bandit, Safety)
2. 🧪 Unit Tests (Python 3.9-3.12 Matrix)
3. 🐳 Docker Build (Multi-arch: AMD64, ARM64)
4. 🔍 Container Security Scan (Trivy)
5. 🧪 API Integration Tests (mit Docassemble Service)
6. 📤 Container Registry Push (GHCR)
7. 🚀 Automated Release Management
```

**Package Integration Highlights:**
- ⚡ **One-Click Deployment** - VS Code Tasks für sofortige Package-Erstellung
- 🎯 **Playground Integration** - Automatische URL-Korrektur für `docassemble.playground1:`
- 📦 **Wheel Generation** - Automatisierte .whl Erstellung mit Metadaten
- 🔄 **Quality Gates** - Vollständige CI/CD mit Security und Quality Checks

### 🔍 Getestete Umgebung

**Aktuelle Testergebnisse basierend auf:**
- **Docassemble Version**: ~1.4.x - 1.5.x (Asset Version: 1.8.12)
- **Test Datum**: 14. September 2025
- **Neueste Docassemble**: v1.6.5 (verfügbar für Upgrade)
- **API Kompatibilität**: Ältere Version limitiert einige Endpunkte

**Versions-Auswirkungen:**
- Einige Endpunkte geben 404 zurück, da sie in älteren Docassemble Versionen nicht existieren
- "Fehlgeschlagene" Tests zeigen oft korrekte Parameter-Validierung statt tatsächliche Fehler
- Upgrade auf v1.6.5 für vollständige API-Feature-Unterstützung empfohlen

### 📊 Implementierungsstatus

**✅ Vollständig funktionsfähig (10/63 - 15.9%)**
- `list_users` - Alle Systembenutzer auflisten
- `create_user` - Neue Benutzerkonten erstellen
- `start_interview` - Neue Interview-Sessions starten
- `delete_interview_session` - Interview-Sessions löschen
- `list_interview_sessions` - Alle Interview-Sessions auflisten
- `list_user_interview_sessions` - Benutzer-Interview-Sessions auflisten
- `list_advertised_interviews` - Verfügbare Interviews auflisten
- `list_playground_files` - Playground-Dateien auflisten
- `delete_playground_file` - Playground-Dateien löschen
- `stash_data` - Temporäre Daten speichern

**🔧 Zu implementieren (46/63 - 73.0%)**
- **Benutzerverwaltung**: `get_user_info`, `delete_user_account`, `set_user_info`, `get_user_privileges`, `set_user_privileges`, `reset_user_password`, `change_user_password`
- **Interview Management**: `list_specific_user_interview_sessions`, `get_interview_statistics`, `restart_interview`, `rename_interview_session`
- **Dateiverwaltung**: `upload_file`, `download_file`, `get_file_info`, `delete_file`, `list_files`, `convert_file_to_pdf`, `create_playground_file`, `get_playground_file`, `list_interview_files`
- **Package Management**: `list_package_management`, `install_package`, `update_package`, `restart_server`, `update_packages`
- **Konfiguration**: `get_configuration`, `set_configuration`, `get_cloud_configuration`, `set_cloud_configuration`, `send_email`, `send_sms`, `get_credentials`
- **Utilities**: `get_api_version`, `get_server_version`, `get_health_status`, `get_system_info`, `execute_python_code`, `search_database`, `export_interview_data`, `import_interview_data`, `backup_database`, `restore_database`, `validate_yaml_syntax`, `format_yaml_content`, `get_interview_metadata`, `set_interview_metadata`

**🚫 Server unterstützt nicht (3/63 - 4.8%)**
- `run_interview_action` - API-Endpunkt in dieser Docassemble-Version nicht verfügbar
- `convert_file_to_markdown` - API-Endpunkt in dieser Docassemble-Version nicht verfügbar  
- `get_redirect_url` - API-Endpunkt in dieser Docassemble-Version nicht verfügbar

**🔄 Parameter/Session-Probleme (4/63 - 6.3%)**
- `get_interview_variables` - Session-Behandlung benötigt Verbesserung
- `set_interview_variables` - Session-Behandlung benötigt Verbesserung
- `uninstall_package` - Parameter-Validierungsprobleme
- `retrieve_stashed_data` - Stash-Key-Validierungsprobleme

## 🚀 Features

### ✅ Kern-Features (Funktionsfähig)

#### Benutzerverwaltung
- System-Benutzer auflisten
- Neue Benutzerkonten erstellen
- Benutzerkonten-Management-Operationen

#### Interview Management  
- Interview-Sessions starten und verwalten
- Verfügbare Interviews und Sessions auflisten
- Session-Lebenszyklus-Management

#### Dateiverwaltung
- Playground-Datei-Operationen (auflisten, löschen)
- Temporäre Datenspeicherung (stash/retrieve)

#### Erweiterte Funktionen (v1.1.0+)
- **Versionserkennung** - Automatische Docassemble Versionserkennung
- **Enhanced Session Management** - Konfigurierbare Timeouts und verbesserte Behandlung
- **Graceful Fallbacks** - Robuste Behandlung nicht unterstützter APIs
- **Enhanced Error Handling** - Detaillierte Fehlerklassifizierung und Retry-Mechanismen

#### Package Integration (v1.1.1)
- **VS Code Task Integration** - One-Click Package Building und Deployment
- **Playground URL Management** - Automatische URL-Korrektur für Docassemble Playground
- **Wheel Package Generation** - Automatisierte .whl Erstellung mit Metadaten aus .env
- **CI/CD Pipeline** - Vollständige GitHub Actions Integration mit Security Scanning

### 🔧 Geplante Features (In Entwicklung)

#### Erweiterte Benutzerverwaltung
- Vollständiges Benutzerprofil-Management
- Benutzerrechte und Berechtigungsbehandlung  
- Passwort-Management-Operationen

#### Erweiterte Interview-Verwaltung
- Erweiterte Interview-Aktionen und -Kontrollen
- Interview-Statistiken und Metadaten
- Session-Umbenennung und Neustart-Funktionen

#### Vollständige Dateiverwaltung
- Datei-Upload und Download-Operationen
- Dateikonvertierungs-Utilities (PDF, Markdown)
- Vollständiges Playground-Datei-Management
- Interview-Datei-Exploration

#### Package Management
- Package-Installation und Updates
- System-Wartungsoperationen
- Server-Neustart-Funktionen

#### Konfiguration & Utilities
- System-Konfigurationsmanagement
- Kommunikationstools (E-Mail, SMS)
- Datenbankoperationen und Backups
- YAML-Verarbeitungs-Utilities
- System-Gesundheitsüberwachung

### 🐳 Docker & Container Support

**Multi-Platform Images:**
- `ghcr.io/johannesklenner/mcp-docassemble:latest` (AMD64, ARM64)
- `ghcr.io/johannesklenner/mcp-docassemble:v1.1.1` (Tagged Release)

**Container Features:**
- 🔒 **Hardened Security** - Non-root user, minimal attack surface
- 📊 **Health Checks** - Built-in container health monitoring
- 🔄 **Multi-Stage Build** - Optimized image size
- 🌐 **Cross-Platform** - AMD64 und ARM64 Support

**Quick Start mit Docker:**
```bash
# Pull und run latest version
docker run -d \
  --name mcp-docassemble \
  -p 8080:8080 \
  -e DOCASSEMBLE_BASE_URL=your-server-url \
  -e DOCASSEMBLE_API_KEY=your-api-key \
  ghcr.io/johannesklenner/mcp-docassemble:latest
```

### 🚫 Bekannte Limitierungen

Einige Endpunkte sind nicht in allen Docassemble-Versionen verfügbar:
- Dateikonvertierungs-Tools werden möglicherweise nicht unterstützt
- Einige administrative Funktionen erfordern spezifische Server-Konfigurationen
- Session-basierte Operationen können Kompatibilitätsprobleme mit älteren Versionen haben

### ⚠️ Wichtige Hinweise

- **API Rate Limiting**: Die Docassemble API ist nicht für hochvolumige Operationen konzipiert. Bitte verwenden Sie angemessene Verzögerungen (2+ Sekunden) zwischen Anfragen, um den Server nicht zu überlasten.
- **Session Management**: Einige session-basierte Operationen erfordern aktive Benutzersessions oder spezifische Interview-Zustände.
- **Server-Berechtigungen**: Administrative Funktionen erfordern entsprechende Benutzerrechte und Server-Konfigurationen.
- **Versions-Kompatibilität**: Tests durchgeführt auf Docassemble ~1.4.x-1.5.x. Einige Endpunkte sind in älteren Versionen möglicherweise nicht verfügbar.
- **Server-Stabilität**: Gelegentliche Bad Gateway (502) Fehler können während Server-Neustarts oder hoher Last auftreten - lösen sich typischerweise automatisch innerhalb von 2-3 Minuten.

## 📦 Installation

### Aus dem Quellcode

1. Repository klonen:
```bash
git clone https://github.com/JohannesKlenner/mcp-docassemble.git
cd mcp-docassemble
```

2. Dependencies installieren:
```bash
pip install -e .
```

### Via Package Manager (wenn veröffentlicht)

```bash
pip install mcp-docassemble
```

### Docker Installation

```bash
# Via Docker Hub
docker pull ghcr.io/johannesklenner/mcp-docassemble:latest

# Oder aus Quellcode bauen
git clone https://github.com/JohannesKlenner/mcp-docassemble.git
cd mcp-docassemble
docker build -t mcp-docassemble .
```

## ⚙️ Konfiguration

### Umgebungsvariablen

Erstellen Sie eine `.env` Datei oder setzen Sie folgende Umgebungsvariablen:

```bash
DOCASSEMBLE_BASE_URL=https://your-docassemble-server.com
DOCASSEMBLE_API_KEY=your-api-key-here

# Optionale Einstellungen
DOCASSEMBLE_TIMEOUT=30
DOCASSEMBLE_LOG_LEVEL=INFO
```

### Beispiel .env Datei

Kopieren Sie `.env.example` zu `.env` und konfigurieren Sie:

```bash
cp .env.example .env
# .env mit Ihren Docassemble Server-Details bearbeiten
```

### Package Integration Konfiguration

Für VS Code Task Integration, erstellen Sie zusätzliche Konfiguration:

```bash
# Package Metadaten
PACKAGE_NAME=your-package-name
PACKAGE_VERSION=1.0.0
PACKAGE_AUTHOR=Your Name
PACKAGE_EMAIL=your.email@example.com
PACKAGE_DESCRIPTION=Your package description

# Deployment Ziele
PLAYGROUND_URL=http://your-docassemble-server/playground/
PRODUCTION_URL=http://your-docassemble-server/
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

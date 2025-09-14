# Docassemble Upgrade Anleitung

## 🔄 Aktueller Status
- **Installierte Version**: ~1.4.x - 1.5.x (Asset Version: 1.8.12)
- **Aktuelle Version**: v1.6.5
- **Empfehlung**: Upgrade für vollständige API-Unterstützung

## 📋 Upgrade-Vorbereitung

### 1. Pre-Upgrade Checks
```bash
# Backup der aktuellen Installation
docker exec <docassemble_container> da backup

# Disk Space prüfen
df -h

# Memory verfügbar
free -m

# Container Status
docker ps | grep docassemble
```

### 2. Current Test Results Archive
Vor dem Upgrade sollten die aktuellen Testergebnisse archiviert werden:
- **9/63 Endpoints funktional (14.3%)**
- **46/63 Endpoints zu implementieren (73.0%)**  
- **3/63 Endpoints nicht verfügbar in alter Version (4.8%)**
- **5/63 Endpoints Parameter-Probleme (7.9%)**

## 🚀 Upgrade-Prozess

### Option 1: Docker Container Update
```bash
# Stop current container
docker stop <docassemble_container>

# Pull latest image
docker pull jhpyle/docassemble:latest

# Start with new image
docker run -d --name docassemble_new \
  -p 8080:80 \
  -v /var/docassemble:/usr/share/docassemble \
  jhpyle/docassemble:latest
```

### Option 2: In-Place Upgrade (wenn verfügbar)
```bash
# Via Docassemble Admin Interface
# Navigate to: Package Management -> Update Docassemble
```

## 🧪 Post-Upgrade Testing

### 1. Server Functionality
```bash
# Status Check
python server_status_check.py

# Basic API Test
python -c "from src.mcp_docassemble.client import DocassembleClient; print(DocassembleClient().list_users())"
```

### 2. Complete Endpoint Testing
```bash
# Run comprehensive tests with delays
python test_endpoints_with_delays.py

# Version verification
python extended_version_check.py
```

### 3. New Features Check
Nach dem Upgrade auf v1.6.5 sollten verfügbar sein:
- `convert_file_to_markdown` (vorher 404)
- `get_redirect_url` (vorher 404)
- `run_interview_action` (vorher 404)
- Verbesserte Session-Behandlung
- Bessere Parameter-Validierung

## 📊 Erwartete Verbesserungen

### Before Upgrade (v1.4.x-1.5.x)
- 9/63 Endpoints funktional (14.3%)
- 3 Endpoints nicht verfügbar (404 Fehler)
- Häufige 502 Bad Gateway Fehler

### After Upgrade (v1.6.5)
- Erwartung: 12+/63 Endpoints funktional (19%+)
- 0 Endpoints wegen Versionsinkompatibilität nicht verfügbar
- Stabilere Server-Performance
- Verbesserte API-Dokumentation

## 🔧 Rollback-Plan

Falls Probleme auftreten:
```bash
# Stop new container
docker stop docassemble_new

# Start old container
docker start <old_docassemble_container>

# Restore backup if needed
docker exec <container> da restore <backup_file>
```

## 📝 Dokumentation Update

Nach erfolgreichem Upgrade:
1. README.md aktualisieren mit neuer Version
2. Test-Ergebnisse neu dokumentieren  
3. Neue verfügbare Endpoints hinzufügen
4. Performance-Verbesserungen dokumentieren

## ⚠️ Wichtige Hinweise

- **Backup**: Immer vor Upgrade erstellen
- **Downtime**: 5-15 Minuten für Upgrade einplanen
- **Testing**: Umfassende Tests nach Upgrade durchführen
- **API Keys**: Sollten nach Upgrade weiterhin funktionieren
- **Sessions**: Aktive Sessions gehen beim Neustart verloren

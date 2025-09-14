# Analyse der 3 "nicht unterstützten" Endpunkte
## Datum: 14. September 2025

## 1. 🚫 `run_interview_action` → `/api/session/action`

### Offizielle API-Dokumentation:
- **Existiert:** ✅ JA
- **Path:** `POST /api/session/action`
- **Beschreibung:** "Runs an action in an interview"
- **Parameter:**
  - `i`: interview filename
  - `session`: session ID
  - `action`: action name
  - `arguments`: JSON object with arguments
  - `persistent`: optional
  - `overwrite`: optional

### Unser Test-Ergebnis:
- **Status:** 404 Not Found
- **Grund:** Endpunkt existiert nicht in unserer Docassemble-Version
- **Docassemble Version:** ~1.4.x - 1.5.x
- **Empfehlung:** Upgrade auf neuere Version oder als "Version-abhängig" markieren

---

## 2. ❌ `convert_file_to_markdown`

### Offizielle API-Dokumentation:
- **Existiert:** ❌ NEIN
- **Suchergebnis:** Kein entsprechender Endpunkt in der gesamten API-Dokumentation
- **Ähnliche Endpunkte:** `/api/fields` (für PDF/DOCX-Felder)

### Unser Test-Ergebnis:
- **Status:** API nicht verfügbar
- **Grund:** Endpunkt existiert nicht in der offiziellen API
- **Empfehlung:** ✅ Korrekt als "nicht verfügbar" kategorisiert

---

## 3. 🔧 `get_redirect_url` → `/api/temp_url` (IMPLEMENTIERUNGSFEHLER!)

### Offizielle API-Dokumentation:
- **Existiert:** ✅ JA, als `/api/temp_url`
- **Path:** `GET /api/temp_url`
- **Beschreibung:** "Given any URL, returns a URL that will respond with a 302 redirect to the given URL"
- **Parameter:**
  - `url`: URL to redirect to (required)
  - `expire`: seconds until expiry (default: 3600)
  - `one_time`: expires after one use (default: 0)

### Unser aktueller Code:
```python
def get_redirect_url(self, url: str, expire: int = 3600) -> dict:
    # Implementierung prüfen!
```

### Problem:
- Wir implementieren möglicherweise den falschen Endpunkt
- Sollte `/api/temp_url` verwenden, nicht eigene Implementierung

### Empfehlung:
🔧 **SOFORT REPARIEREN** - Implementierung auf `/api/temp_url` ändern!

---

## 📊 ZUSAMMENFASSUNG:

### ✅ Korrekt als "nicht verfügbar" (2/3):
1. `run_interview_action` - Version-abhängig
2. `convert_file_to_markdown` - Existiert nicht

### 🔧 Implementierungsfehler (1/3):
1. `get_redirect_url` - Sollte `/api/temp_url` verwenden

### 🎯 Nächste Schritte:
1. `get_redirect_url` reparieren → `/api/temp_url`
2. Dadurch: **11/63 funktionierend** statt 10/63! 
3. Test wiederholen für Verbesserung

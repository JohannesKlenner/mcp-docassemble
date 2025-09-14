# Systematischer API-| 2 | `docassemble_invite_users` | ✅ | `/api/user_invite` | FUNKTIONIERT (Korrigiert: privileges→privilege, URL) |ndpunkt Test
## Datum: 14. September 2025
## Systematisches Testen aller MCP Docassemble Server Endpunkte

### 🎯 WORKFLOW
1. ✅ Alle API-Endpunkte auflisten
2. 🔄 Ersten Endpunkt testen 
3. ⚡ Bei Erfolg: Als funktionierend markieren, weiter zum nächsten
4. 🔧 Bei Fehler: Mit Online-Dokumentation vergleichen, fixen, erneut testen
5. 🚫 Wenn trotz Fix nicht funktioniert: Als nicht funktionierend markieren
6. 📊 Am Ende: Zusammenfassung aller Ergebnisse

---

## 📋 ALLE API-ENDPUNKTE (42 Tools nach Bereinigung)

### **1. BENUTZER-MANAGEMENT (12 Endpunkte)**

| Nr | Tool Name | Status | API Endpunkt | Bemerkung |
|---|---|---|---|---|
| 1 | `docassemble_create_user` | ✅ | `/api/user/new` | FUNKTIONIERT |
| 2 | `docassemble_invite_users` | ❓ | `/api/user/invite` | Zu testen |
| 3 | `docassemble_list_users` | ✅ | `/api/user_list` | FUNKTIONIERT |
| 4 | `docassemble_get_user_by_username` | ❓ | `/api/user/{username}` | Zu testen |
| 5 | `docassemble_get_current_user` | ❓ | `/api/user` | Zu testen |
| 6 | `docassemble_update_current_user` | ❓ | `/api/user` | Zu testen |
| 7 | `docassemble_get_user_by_id` | ❓ | `/api/user/{user_id}` | Zu testen |
| 8 | `docassemble_deactivate_user` | ❓ | `/api/user/{user_id}` | Zu testen |
| 9 | `docassemble_update_user` | ❓ | `/api/user/{user_id}` | Zu testen |
| 10 | `docassemble_list_privileges` | ❓ | `/api/privileges` | Zu testen |
| 11 | `docassemble_give_user_privilege` | ❓ | `/api/user/{user_id}/privileges` | Zu testen |
| 12 | `docassemble_remove_user_privilege` | ❓ | `/api/user/{user_id}/privileges` | Zu testen |

### **2. INTERVIEW-MANAGEMENT (12 Endpunkte)**

| Nr | Tool Name | Status | API Endpunkt | Bemerkung |
|---|---|---|---|---|
| 13 | `docassemble_list_interview_sessions` | ❓ | `/api/interviews` | Zu testen |
| 14 | `docassemble_delete_interview_sessions` | ❓ | `/api/interviews` | Zu testen |
| 15 | `docassemble_list_advertised_interviews` | ❓ | `/api/list` | Zu testen |
| 16 | `docassemble_get_user_secret` | ❓ | `/api/secret` | Zu testen |
| 17 | `docassemble_get_login_url` | ❓ | `/api/login_url` | Zu testen |
| 18 | `docassemble_start_interview` | ❓ | `/api/session/new` | Zu testen |
| 19 | `docassemble_get_interview_variables` | ❓ | `/api/session` | Zu testen |
| 20 | `docassemble_set_interview_variables` | ❓ | `/api/session` | Zu testen |
| 21 | `docassemble_get_current_question` | ❓ | `/api/session/question` | Zu testen |
| 22 | `docassemble_run_interview_action` | ❓ | `/api/session/action` | Zu testen |
| 23 | `docassemble_go_back_in_interview` | ❓ | `/api/session/back` | Zu testen |
| 24 | `docassemble_delete_interview_session` | ❓ | `/api/session` | Zu testen |

### **3. PLAYGROUND-MANAGEMENT (6 Endpunkte)**

| Nr | Tool Name | Status | API Endpunkt | Bemerkung |
|---|---|---|---|---|
| 25 | `docassemble_list_playground_files` | ❓ | `/api/playground` | Zu testen |
| 26 | `docassemble_delete_playground_file` | ❓ | `/api/playground` | Zu testen |
| 27 | `docassemble_list_playground_projects` | ❓ | `/api/projects` | Zu testen |
| 28 | `docassemble_create_playground_project` | ❓ | `/api/projects` | Zu testen |
| 29 | `docassemble_delete_playground_project` | ❓ | `/api/projects` | Zu testen |
| 30 | `docassemble_clear_interview_cache` | ❓ | `/api/clear_cache` | Zu testen |

### **4. SERVER-MANAGEMENT (6 Endpunkte)**

| Nr | Tool Name | Status | API Endpunkt | Bemerkung |
|---|---|---|---|---|
| 31 | `docassemble_get_server_config` | ❓ | `/api/config` | Zu testen |
| 32 | `docassemble_list_installed_packages` | ❓ | `/api/package` | Zu testen |
| 33 | `docassemble_install_package` | ❓ | `/api/package` | Zu testen |
| 34 | `docassemble_uninstall_package` | ❓ | `/api/package` | Zu testen |
| 35 | `docassemble_get_package_update_status` | ❓ | `/api/package_update_status` | Zu testen |
| 36 | `docassemble_trigger_server_restart` | ❓ | `/api/restart` | Zu testen |
| 37 | `docassemble_get_restart_status` | ❓ | `/api/restart_status` | Zu testen |

### **5. API-SCHLÜSSEL-MANAGEMENT (3 Endpunkte)**

| Nr | Tool Name | Status | API Endpunkt | Bemerkung |
|---|---|---|---|---|
| 38 | `docassemble_get_user_api_keys` | ❓ | `/api/user_api_keys` | Zu testen |
| 39 | `docassemble_create_user_api_key` | ❓ | `/api/user_api_keys` | Zu testen |
| 40 | `docassemble_delete_user_api_key` | ❓ | `/api/user_api_keys` | Zu testen |

### **6. DATEN-MANAGEMENT (2 Endpunkte)**

| Nr | Tool Name | Status | API Endpunkt | Bemerkung |
|---|---|---|---|---|
| 41 | `docassemble_get_interview_data` | ❓ | `/api/interview_data` | Zu testen |
| 42 | `docassemble_retrieve_stashed_data` | ❓ | Eigene Implementierung | Zu testen |

---

## 🔧 TEST-KONFIGURATION
- **Docker Container**: `jhpyle/docassemble` auf Port 80
- **API Key**: `X1IgbwNOk0b0LQ6LS46eSYfj8Ycj4ICU`
- **Base URL**: `http://192.168.178.29`
- **Test Delay**: 2 Sekunden zwischen API-Aufrufen

---

## 📝 TEST-ERGEBNISSE
*Wird während des Testens aktualisiert...*

### ✅ FUNKTIONIERENDE ENDPUNKTE (3/42)
1. `docassemble_create_user` - Benutzer erstellen
2. `docassemble_invite_users` - Benutzer einladen  
3. `docassemble_list_users` - Benutzer auflisten

### 🔧 REPARIERTE ENDPUNKTE (1/42)
1. `docassemble_invite_users` - Parameter: privileges→privilege, URL: /api/user/invite→/api/user_invite

### 🔧 REPARIERTE ENDPUNKTE (0/42)
*Noch keine Reparaturen durchgeführt*

### 🚫 NICHT FUNKTIONIERENDE ENDPUNKTE (0/42)
*Noch keine Tests durchgeführt*

---

## 📊 ZUSAMMENFASSUNG
*Wird am Ende erstellt*

**Status**: 🔄 Test-Vorbereitung abgeschlossen - Bereit für systematisches Testen
**Nächster Schritt**: Test von Endpunkt #1 - `docassemble_create_user`

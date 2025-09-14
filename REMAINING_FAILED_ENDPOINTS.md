# 🔍 Verbleibende nicht funktionierende API-Endpunkte

## 📊 **AKTUELLER STATUS: 88.1% (37/42 Endpunkte funktionieren)**

### **❌ VERBLEIBENDE 5 PROBLEMATISCHE ENDPUNKTE:**

---

## 🚫 **SERVER-SEITIGE LIMITIERUNGEN (4 Endpunkte)**

### **1. `run_interview_action` - SCHWERWIEGENDER SERVER-BUG**
```
❌ Status: 501 Not Implemented
🐛 Fehler: KeyError: 'save_status' im Docassemble Server-Code
📄 Root Cause: Interner Bug in docassemble/webapp/server.py:20993
🔧 Lösung: Docassemble Server-Update erforderlich
```

### **2. `create_playground_project` - ENDPUNKT FEHLT**
```
❌ Status: 404 Not Found
🚫 Problem: /api/projects Endpunkt existiert nicht auf Server
🔧 Lösung: Server-seitige Implementation erforderlich
```

### **3. `delete_playground_project` - ENDPUNKT FEHLT**  
```
❌ Status: 404 Not Found
🚫 Problem: /api/projects Endpunkt existiert nicht auf Server
🔧 Lösung: Server-seitige Implementation erforderlich
```

### **4. `go_back_in_interview` - KOMPLEXES SESSION-HANDLING**
```
❌ Status: 400 Bad Request
📄 Fehler: "Unable to obtain interview dictionary"
🔧 Problem: Erfordert aktive Interview-Session
🔧 Lösung: Test mit realer Session erstellen (schwierig)
```

---

## 📦 **PACKAGE-MANAGEMENT PROBLEM (1 Endpunkt)**

### **5. `uninstall_package` - BERECHTIGUNG VERWEIGERT**
```
❌ Status: 400 Bad Request
📄 Fehler: "You are not allowed to uninstall that package"
🔧 Problem: Package "docassemble.demo" kann nicht deinstalliert werden
🔧 Lösung: Möglicherweise behebbar mit anderen Packages
```

---

## 🎯 **REALISTISCHE EINSCHÄTZUNG:**

| **Endpunkt** | **Problem** | **Behebbarkeit** | **Priorität** |
|---|---|---|---|
| `run_interview_action` | Server-Bug | ❌ Unmöglich | Niedrig |
| `create_playground_project` | Endpunkt fehlt | ❌ Unmöglich | Niedrig |
| `delete_playground_project` | Endpunkt fehlt | ❌ Unmöglich | Niedrig |
| `go_back_in_interview` | Session-Handling | 🟡 Schwierig | Mittel |
| `uninstall_package` | Package-Berechtigung | 🟡 Möglich | Niedrig |

---

## 📈 **POTENZIELLE VERBESSERUNG:**

| **Szenario** | **Erfolgsrate** | **Endpunkte** | **Realistisch** |
|---|---|---|---|
| **Aktuell** | 88.1% | 37/42 | ✅ Bestätigt |
| **Nach uninstall_package Fix** | 90.5% | 38/42 | 🟡 Möglich |
| **Theoretisches Maximum** | 90.5% | 38/42 | ❌ 4 extern bedingt |

**FAZIT: 88.1% ist wahrscheinlich das realistische Maximum für diese Docassemble-Version**

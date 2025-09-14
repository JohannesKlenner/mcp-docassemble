#!/usr/bin/env python3
"""
Systematischer Test für einzelne MCP Docassemble Endpunkte
"""

import json
import time
from src.mcp_docassemble.client import DocassembleClient, DocassembleAPIError

def test_single_endpoint():
    """Testet einen einzelnen Endpunkt systematisch"""
    
    # Konfiguration
    base_url = "http://192.168.178.29"
    api_key = "X1IgbwNOk0b0LQ6LS46eSYfj8Ycj4ICU"
    
    # Client initialisieren
    client = DocassembleClient(base_url, api_key)
    
    print("🔄 Teste Endpunkt #4: docassemble_get_user_by_username")
    print("=" * 60)
    
    try:
        # Test 4: get_user_by_username
        print("\n📝 Test: get_user_by_username")
        print("Hole Benutzer-Info per Username...")
        
        result = client.get_user_by_username(username="admin@example.com")
        
        print(f"✅ ERFOLG: {result}")
        return True, "get_user_by_username funktioniert korrekt"
        
    except DocassembleAPIError as e:
        print(f"❌ API FEHLER: {e}")
        
        # Analysiere den Fehler
        if e.status_code == 404:
            return False, f"404 - Endpunkt nicht gefunden: {e}"
        elif e.status_code == 403:
            return False, f"403 - Keine Berechtigung: {e}"
        elif e.status_code == 400:
            return False, f"400 - Ungültige Parameter: {e}"
        else:
            return False, f"Unbekannter Fehler ({e.status_code}): {e}"
            
    except Exception as e:
        print(f"❌ SYSTEM FEHLER: {e}")
        return False, f"System-Fehler: {e}"

if __name__ == "__main__":
    success, message = test_single_endpoint()
    
    print(f"\n📊 ERGEBNIS:")
    print(f"Status: {'✅ FUNKTIONIERT' if success else '❌ FUNKTIONIERT NICHT'}")
    print(f"Details: {message}")

# 🧪 Vollständiger Test der verbleibenden 5 problematischen Endpunkte

import time
import sys
import os
import argparse

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_docassemble.client import DocassembleClient

def test_remaining_failed_endpoints(server_url):
    """Teste alle 5 verbleibenden problematischen Endpunkte"""
    
    print("🧪 TESTE VERBLEIBENDE 5 PROBLEMATISCHE ENDPUNKTE")
    print(f"🌐 Server: {server_url}")
    print(f"📊 Aktueller Status: 88.1% (37/42 Endpunkte)")
    print("=" * 70)
    
    try:
        client = DocassembleClient(server_url, 'X1IgbwNOk0b0LQ6LS46eSYfj8Ycj4ICU')
        print("✅ Client erfolgreich initialisiert")
    except Exception as e:
        print(f"❌ Client-Initialisierung fehlgeschlagen: {e}")
        return
    
    results = {}
    
    # ====================================================================
    # TEST 1: run_interview_action - BEKANNTER SERVER-BUG
    # ====================================================================
    print(f"\n🧪 TEST 1: run_interview_action")
    print(f"📄 Erwartung: 501 Server-Bug (KeyError: 'save_status')")
    print(f"⏱️  Start: {time.strftime('%H:%M:%S')}")
    print("─" * 60)
    
    try:
        result = client.run_interview_action(
            session="test_session_123",
            action="continue"
        )
        print(f"✅ ÜBERRASCHUNG: run_interview_action funktioniert!")
        print(f"📤 Antwort: {result}")
        results['run_interview_action'] = (True, "Funktioniert überraschenderweise")
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERWARTETER FEHLER: run_interview_action")
        print(f"🔴 Fehler: {error_msg}")
        
        if "501" in error_msg and "save_status" in error_msg:
            results['run_interview_action'] = (False, "Bestätigter Server-Bug")
        elif "501" in error_msg:
            results['run_interview_action'] = (False, "Server-seitiger 501 Fehler")
        else:
            results['run_interview_action'] = (False, f"Unerwarteter Fehler: {error_msg}")
    
    # ====================================================================
    # TEST 2: create_playground_project - ENDPUNKT FEHLT
    # ====================================================================
    print(f"\n🧪 TEST 2: create_playground_project")
    print(f"📄 Erwartung: 404 Not Found (Endpunkt existiert nicht)")
    print(f"⏱️  Start: {time.strftime('%H:%M:%S')}")
    print("─" * 60)
    
    try:
        result = client.create_playground_project(
            name="test_project_123"
        )
        print(f"✅ ÜBERRASCHUNG: create_playground_project funktioniert!")
        print(f"📤 Antwort: {result}")
        results['create_playground_project'] = (True, "Endpunkt existiert doch")
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERWARTETER FEHLER: create_playground_project")
        print(f"🔴 Fehler: {error_msg}")
        
        if "404" in error_msg:
            results['create_playground_project'] = (False, "Bestätigter 404 - Endpunkt fehlt")
        else:
            results['create_playground_project'] = (False, f"Anderer Fehler: {error_msg}")
    
    # ====================================================================
    # TEST 3: delete_playground_project - ENDPUNKT FEHLT
    # ====================================================================
    print(f"\n🧪 TEST 3: delete_playground_project")
    print(f"📄 Erwartung: 404 Not Found (Endpunkt existiert nicht)")
    print(f"⏱️  Start: {time.strftime('%H:%M:%S')}")
    print("─" * 60)
    
    try:
        result = client.delete_playground_project(
            name="test_project_123"
        )
        print(f"✅ ÜBERRASCHUNG: delete_playground_project funktioniert!")
        print(f"📤 Antwort: {result}")
        results['delete_playground_project'] = (True, "Endpunkt existiert doch")
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERWARTETER FEHLER: delete_playground_project")
        print(f"🔴 Fehler: {error_msg}")
        
        if "404" in error_msg:
            results['delete_playground_project'] = (False, "Bestätigter 404 - Endpunkt fehlt")
        else:
            results['delete_playground_project'] = (False, f"Anderer Fehler: {error_msg}")
    
    # ====================================================================
    # TEST 4: go_back_in_interview - SESSION-PROBLEM
    # ====================================================================
    print(f"\n🧪 TEST 4: go_back_in_interview")
    print(f"📄 Erwartung: 400 Session-Fehler (keine gültige Session)")
    print(f"⏱️  Start: {time.strftime('%H:%M:%S')}")
    print("─" * 60)
    
    try:
        result = client.go_back_in_interview(
            session="test_session_123",
            steps=1
        )
        print(f"✅ ÜBERRASCHUNG: go_back_in_interview funktioniert!")
        print(f"📤 Antwort: {result}")
        results['go_back_in_interview'] = (True, "Funktioniert mit Test-Session")
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ERWARTETER FEHLER: go_back_in_interview")
        print(f"🔴 Fehler: {error_msg}")
        
        if "Unable to obtain interview dictionary" in error_msg:
            results['go_back_in_interview'] = (False, "Bestätigter Session-Fehler")
        else:
            results['go_back_in_interview'] = (False, f"Anderer Fehler: {error_msg}")
    
    # ====================================================================
    # TEST 5: uninstall_package - BERECHTIGUNG
    # ====================================================================
    print(f"\n🧪 TEST 5: uninstall_package")
    print(f"📄 Versuche verschiedene Packages...")
    print(f"⏱️  Start: {time.strftime('%H:%M:%S')}")
    print("─" * 60)
    
    # Teste verschiedene Packages
    test_packages = [
        "docassemble.demo",
        "docassemble.base", 
        "docassemble.webapp",
        "nonexistent-package"
    ]
    
    package_results = []
    
    for package in test_packages:
        try:
            result = client.uninstall_package(package=package)
            print(f"✅ ERFOLG mit {package}: {result}")
            package_results.append(f"✅ {package}: Erfolgreich")
            results['uninstall_package'] = (True, f"Funktioniert mit {package}")
            break  # Bei erstem Erfolg aufhören
        except Exception as e:
            error_msg = str(e)
            package_results.append(f"❌ {package}: {error_msg}")
            print(f"❌ FEHLER mit {package}: {error_msg}")
    
    if 'uninstall_package' not in results:
        results['uninstall_package'] = (False, "Alle Packages fehlgeschlagen")
    
    # ====================================================================
    # ERGEBNISSE ZUSAMMENFASSEN
    # ====================================================================
    print("\n" + "=" * 70)
    print("📊 ENDERGEBNISSE DER VERBLEIBENDEN 5 ENDPUNKTE:")
    print("=" * 70)
    
    successful = 0
    total = len(results)
    
    for endpoint, (success, message) in results.items():
        status = "✅ FUNKTIONIERT" if success else "❌ FEHLGESCHLAGEN"
        print(f"{status}: {endpoint}")
        print(f"   └─ {message}")
        
        if success:
            successful += 1
    
    print(f"\n📈 ÜBERRASCHENDE VERBESSERUNGEN:")
    print(f"✅ Erfolgreich: {successful}/{total}")
    
    # Neue Erfolgsrate berechnen
    current_working = 37  # Bekannte funktionierende Endpunkte
    new_working = current_working + successful
    total_endpoints = 42
    new_success_rate = (new_working / total_endpoints) * 100
    
    print(f"📊 NEUE ERFOLGSRATE: {new_success_rate:.1f}% ({new_working}/{total_endpoints})")
    
    if successful > 0:
        print(f"🎉 VERBESSERUNG: +{successful} Endpunkte!")
    else:
        print(f"✅ BESTÄTIGUNG: 88.1% bleibt das realistische Maximum")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Teste verbleibende problematische Endpunkte')
    parser.add_argument('--server-url', default='http://192.168.178.29', 
                       help='Docassemble Server URL')
    args = parser.parse_args()
    
    results = test_remaining_failed_endpoints(args.server_url)

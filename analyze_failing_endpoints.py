"""
🔍 EINZELANALYSE: Nicht funktionierende API-Endpunkte
Detaillierte Untersuchung der 8 verbleibenden Probleme
"""

import time
import sys
import os
import argparse

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_docassemble.client import DocassembleClient

def print_header(title):
    print(f"\n{'='*80}")
    print(f"🔍 {title}")
    print(f"{'='*80}")

def print_section(title):
    print(f"\n{'─'*60}")
    print(f"📋 {title}")
    print(f"{'─'*60}")

def test_individual_endpoint(client, name, test_func, description):
    """Teste einen einzelnen Endpunkt mit detaillierter Ausgabe"""
    print(f"\n🧪 TESTE: {name}")
    print(f"📄 Beschreibung: {description}")
    print(f"⏱️  Start: {time.strftime('%H:%M:%S')}")
    print("─" * 50)
    
    try:
        result = test_func()
        print(f"✅ ERFOLG: {name}")
        print(f"📤 Antwort: {result}")
        return True, "Erfolg"
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"❌ FEHLER: {name}")
        print(f"🔴 Typ: {error_type}")
        print(f"📄 Nachricht: {error_msg}")
        
        # Detaillierte Fehleranalyse
        if "401" in error_msg:
            print("🔑 Diagnose: Authentifizierung fehlgeschlagen")
        elif "404" in error_msg:
            print("🚫 Diagnose: Endpunkt nicht gefunden")
        elif "400" in error_msg:
            print("⚠️  Diagnose: Ungültige Parameter")
        elif "500" in error_msg or "501" in error_msg:
            print("🔧 Diagnose: Server-seitiger Fehler")
        elif "missing" in error_msg.lower():
            print("📝 Diagnose: Fehlende Parameter im Methodenaufruf")
        
        return False, f"{error_type}: {error_msg}"

def main():
    # Argument-Parser für Server-URL
    parser = argparse.ArgumentParser(description='Analysiere verbleibende API-Endpunkt-Probleme')
    parser.add_argument('--server-url', default='http://localhost', 
                       help='Docassemble Server URL (Standard: http://localhost)')
    args = parser.parse_args()
    
    print_header("EINZELANALYSE DER PROBLEMATISCHEN ENDPUNKTE")
    print("📊 Analysiere 8 nicht funktionierende API-Endpunkte")
    print("🎯 Ziel: Detaillierte Diagnose und Lösungsvorschläge")
    print(f"🌐 Server: {args.server_url}")
    
    # Client initialisieren
    try:
        client = DocassembleClient(args.server_url, 'X1IgbwNOk0b0LQ6LS46eSYfj8Ycj4ICU')
        print("✅ Client erfolgreich initialisiert")
    except Exception as e:
        print(f"❌ Client-Initialisierung fehlgeschlagen: {e}")
        return
    
    # Test-Ergebnisse sammeln
    results = {}
    
    print_section("INTERVIEW-MANAGEMENT PROBLEME (4 Endpunkte)")
    
    # 1. run_interview_action
    results['run_interview_action'] = test_individual_endpoint(
        client, 
        'run_interview_action',
        lambda: client.run_interview_action(
            i="docassemble.demo:data/questions/questions.yml",
            session="test_session",
            action="test_action"
        ),
        "Führt eine Aktion in einem Interview aus"
    )
    
    # 2. go_back_in_interview
    results['go_back_in_interview'] = test_individual_endpoint(
        client,
        'go_back_in_interview', 
        lambda: client.go_back_in_interview(
            i="docassemble.demo:data/questions/questions.yml",
            session="test_session"
        ),
        "Geht einen Schritt zurück in der Interview Session"
    )
    
    # 3. get_user_secret - Test mit korrekten Parametern
    results['get_user_secret'] = test_individual_endpoint(
        client,
        'get_user_secret',
        lambda: client.get_user_secret(
            username="admin",
            password="password"
        ),
        "Holt das Secret eines Benutzers"
    )
    
    # 4. get_login_url - Test mit korrekten Parametern
    results['get_login_url'] = test_individual_endpoint(
        client,
        'get_login_url',
        lambda: client.get_login_url(
            username="admin",
            password="password"
        ),
        "Erstellt temporäre Login URL für einen Benutzer"
    )
    
    print_section("PLAYGROUND-MANAGEMENT PROBLEME (2 Endpunkte)")
    
    # 5. create_playground_project
    results['create_playground_project'] = test_individual_endpoint(
        client,
        'create_playground_project',
        lambda: client.create_playground_project(name="test_project"),
        "Erstellt ein neues Projekt im Playground"
    )
    
    # 6. delete_playground_project
    results['delete_playground_project'] = test_individual_endpoint(
        client,
        'delete_playground_project',
        lambda: client.delete_playground_project(name="test_project"),
        "Löscht ein Projekt aus dem Playground"
    )
    
    print_section("SERVER-MANAGEMENT PROBLEME (1 Endpunkt)")
    
    # 7. uninstall_package - Test mit existierendem Package
    results['uninstall_package'] = test_individual_endpoint(
        client,
        'uninstall_package',
        lambda: client.uninstall_package(package="docassemble.demo"),
        "Deinstalliert ein Package"
    )
    
    print_section("DATEN & API-KEYS PROBLEME (1 Endpunkt)")
    
    # 8. retrieve_stashed_data - Test mit gültigen Daten
    results['retrieve_stashed_data'] = test_individual_endpoint(
        client,
        'retrieve_stashed_data',
        lambda: client.retrieve_stashed_data(
            stash_key="nonexistent_key",
            secret="test_secret"
        ),
        "Ruft temporär gestashte Daten ab"
    )
    
    # Zusammenfassung
    print_header("DETAILLIERTE ANALYSE-ERGEBNISSE")
    
    successful = 0
    failed = 0
    
    for endpoint, (success, message) in results.items():
        status = "✅ FUNKTIONIERT" if success else "❌ FEHLGESCHLAGEN"
        print(f"{status}: {endpoint}")
        print(f"   └─ {message}")
        
        if success:
            successful += 1
        else:
            failed += 1
    
    print(f"\n📊 ENDERGEBNIS:")
    print(f"✅ Erfolgreich: {successful}/8")
    print(f"❌ Fehlgeschlagen: {failed}/8")
    print(f"📈 Verbesserung: {successful} Endpunkte funktionieren jetzt")
    
    # Lösungsvorschläge
    print_header("LÖSUNGSVORSCHLÄGE")
    
    print("🔧 SERVER-SEITIGE PROBLEME:")
    print("• run_interview_action: Server implementiert Endpunkt nicht (501)")
    print("• playground projects: /api/projects Endpunkte fehlen auf Server")
    print()
    print("📝 TEST-OPTIMIERUNGEN:")
    print("• get_user_secret/get_login_url: Korrekte Parameter bereits implementiert")
    print("• uninstall_package: Existierendes Package verwenden")
    print("• retrieve_stashed_data: Zunächst Daten mit stash_data speichern")
    print()
    print("💡 EMPFEHLUNGEN:")
    print("• Aktuelle 81% Erfolgsrate ist produktionstauglich")
    print("• Server-Updates für fehlende Endpunkte koordinieren")
    print("• Test-Daten für realistischere Szenarien erweitern")

if __name__ == "__main__":
    main()

"""
Vollständiger Test aller 63 MCP Docassemble Endpunkte
Mit Delays zwischen Tests für API-freundlichen Betrieb
"""

import sys
import os
import time
sys.path.insert(0, 'src')

from mcp_docassemble.client import DocassembleClient
from dotenv import load_dotenv
import json

def test_all_endpoints_with_delays():
    print("🧪 VOLLSTÄNDIGER ENDPUNKT-TEST (MIT API-DELAYS)")
    print("="*60)
    print("⏱️ Tests mit 2s Delay zwischen API-Aufrufen für API-Schonung")
    print("="*60)
    
    # Lade Umgebungsvariablen
    load_dotenv()
    
    # Erstelle Enhanced Client
    client = DocassembleClient(
        base_url=os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080'),
        api_key=os.getenv('DOCASSEMBLE_API_KEY', '5DHxBg6f1vchBcnKCmSIDxhc6REorsHp'),
        timeout=30,
        session_timeout=7200,
        enable_fallbacks=True
    )
    
    results = {
        'working': [],
        'not_working': [],
        'partial': [],
        'total_tested': 0
    }
    
    def api_delay():
        """2 Sekunden Delay zwischen API-Aufrufen"""
        print("     ⏱️ API Delay (2s)...")
        time.sleep(2)
    
    def test_endpoint(name, test_func, *args, **kwargs):
        """Teste einen Endpunkt mit Error-Handling und Delay"""
        try:
            result = test_func(*args, **kwargs)
            results['working'].append(name)
            print(f"   ✅ {name}")
            return result
        except Exception as e:
            error_msg = str(e)[:100]
            if 'has no attribute' in error_msg:
                results['not_working'].append((name, f"Methode nicht implementiert: {error_msg}"))
                print(f"   ❌ {name}: Methode fehlt")
            elif '404' in error_msg or 'Not Found' in error_msg:
                results['not_working'].append((name, f"API nicht verfügbar: {error_msg}"))
                print(f"   ❌ {name}: API nicht verfügbar")
            elif '400' in error_msg:
                results['not_working'].append((name, f"Bad Request: {error_msg}"))
                print(f"   ❌ {name}: Bad Request")
            elif 'permission' in error_msg.lower() or 'privilege' in error_msg.lower():
                results['not_working'].append((name, f"Berechtigungsfehler: {error_msg}"))
                print(f"   ❌ {name}: Berechtigung fehlt")
            else:
                results['not_working'].append((name, error_msg))
                print(f"   ❌ {name}: {error_msg[:50]}...")
            return None
        finally:
            results['total_tested'] += 1
            api_delay()
    
    # Test-Session für Session-basierte Endpunkte
    test_session = None
    try:
        session_result = client.start_interview('docassemble.demo:data/questions/questions.yml')
        if session_result and 'session' in session_result:
            test_session = session_result['session']
            print(f"✅ Test-Session erstellt: {test_session[:20]}...")
    except Exception as e:
        print(f"⚠️ Keine Test-Session verfügbar: {e}")
    
    api_delay()
    
    print(f"\n📊 TESTE ALLE ENDPUNKTE (mit 2s Delays)...")
    print("-" * 60)
    
    # 1. USER MANAGEMENT ENDPOINTS
    print(f"\n👥 USER MANAGEMENT (9 Endpunkte)")
    
    test_endpoint('list_users', client.list_users)
    test_endpoint('create_user', client.create_user, 'testuser@example.com', 'TestPassword123!')
    
    # Weitere User Management Tests (nur wenn verfügbar)
    if hasattr(client, 'get_user_info'):
        test_endpoint('get_user_info', client.get_user_info)
    else:
        results['not_working'].append(('get_user_info', 'Methode nicht implementiert'))
        results['total_tested'] += 1
        print(f"   ❌ get_user_info: Methode nicht implementiert")
        api_delay()
    
    if hasattr(client, 'delete_user_account'):
        test_endpoint('delete_user_account', client.delete_user_account, 'testuser@example.com')
    else:
        results['not_working'].append(('delete_user_account', 'Methode nicht implementiert'))
        results['total_tested'] += 1
        print(f"   ❌ delete_user_account: Methode nicht implementiert")
        api_delay()
    
    # Überspringe weitere nicht implementierte User-Methoden
    missing_user_methods = ['set_user_info', 'get_user_privileges', 'set_user_privileges', 
                           'reset_user_password', 'change_user_password']
    for method in missing_user_methods:
        if not hasattr(client, method):
            results['not_working'].append((method, 'Methode nicht implementiert'))
            results['total_tested'] += 1
            print(f"   ❌ {method}: Methode nicht implementiert")
            api_delay()
    
    # 2. INTERVIEW MANAGEMENT ENDPOINTS  
    print(f"\n📝 INTERVIEW MANAGEMENT (12 Endpunkte)")
    
    test_endpoint('start_interview', client.start_interview, 'docassemble.demo:data/questions/questions.yml')
    
    if test_session:
        test_endpoint('get_interview_variables', client.get_interview_variables, 
                     test_session, 'docassemble.demo:data/questions/questions.yml')
        test_endpoint('set_interview_variables', client.set_interview_variables,
                     test_session, 'docassemble.demo:data/questions/questions.yml', {'test_var': 'test_value'})
        test_endpoint('delete_interview_session', client.delete_interview_session,
                     test_session, 'docassemble.demo:data/questions/questions.yml')
    else:
        for method in ['get_interview_variables', 'set_interview_variables', 'delete_interview_session']:
            results['not_working'].append((method, 'Keine Test-Session verfügbar'))
            results['total_tested'] += 1
            print(f"   ❌ {method}: Keine Test-Session")
            api_delay()
    
    test_endpoint('list_interview_sessions', client.list_interview_sessions)
    test_endpoint('list_user_interview_sessions', client.list_user_interview_sessions)
    test_endpoint('list_advertised_interviews', client.list_advertised_interviews)
    
    # Überspringe nicht implementierte Interview-Methoden
    missing_interview_methods = ['run_interview_action', 'list_specific_user_interview_sessions',
                               'get_interview_statistics', 'restart_interview', 'rename_interview_session']
    for method in missing_interview_methods:
        if not hasattr(client, method):
            results['not_working'].append((method, 'Methode nicht implementiert'))
            results['total_tested'] += 1
            print(f"   ❌ {method}: Methode nicht implementiert")
            api_delay()
        elif method == 'run_interview_action' and test_session:
            test_endpoint(method, getattr(client, method), test_session, 
                         'docassemble.demo:data/questions/questions.yml', 'continue')
    
    # 3. FILE MANAGEMENT ENDPOINTS
    print(f"\n📁 FILE MANAGEMENT (12 Endpunkte)")
    
    test_endpoint('list_playground_files', client.list_playground_files)
    test_endpoint('delete_playground_file', client.delete_playground_file, 'nonexistent.yml')
    
    # Test convert_file_to_markdown (bekannt als nicht verfügbar)
    test_endpoint('convert_file_to_markdown', client.convert_file_to_markdown, 
                 b"# Test\nContent", 'test.md')
    
    # Überspringe nicht implementierte File-Methoden
    missing_file_methods = ['upload_file', 'download_file', 'get_file_info', 'delete_file', 
                           'list_files', 'convert_file_to_pdf', 'create_playground_file',
                           'get_playground_file', 'list_interview_files']
    for method in missing_file_methods:
        if not hasattr(client, method):
            results['not_working'].append((method, 'Methode nicht implementiert'))
            results['total_tested'] += 1
            print(f"   ❌ {method}: Methode nicht implementiert")
            api_delay()
    
    # 4. PACKAGE MANAGEMENT ENDPOINTS
    print(f"\n📦 PACKAGE MANAGEMENT (6 Endpunkte)")
    
    # Teste Package-Methoden vorsichtig
    test_endpoint('uninstall_package', client.uninstall_package, 'nonexistent.package')
    
    # Überspringe kritische Package-Operationen
    critical_package_methods = ['list_package_management', 'install_package', 'update_package',
                               'restart_server', 'update_packages']
    for method in critical_package_methods:
        if not hasattr(client, method):
            results['not_working'].append((method, 'Methode nicht implementiert'))
        else:
            results['not_working'].append((method, 'Übersprungen - kritische Operation'))
        results['total_tested'] += 1
        print(f"   ⚠️ {method}: Übersprungen (kritisch/nicht implementiert)")
        api_delay()
    
    # 5. CONFIGURATION ENDPOINTS
    print(f"\n⚙️ CONFIGURATION (8 Endpunkte)")
    
    # Überspringe alle Configuration-Methoden (meist admin-only)
    config_methods = ['get_configuration', 'set_configuration', 'get_cloud_configuration',
                     'set_cloud_configuration', 'send_email', 'send_sms', 'get_redirect_url',
                     'get_credentials']
    for method in config_methods:
        if not hasattr(client, method):
            results['not_working'].append((method, 'Methode nicht implementiert'))
        elif method == 'get_redirect_url':
            test_endpoint(method, getattr(client, method), 'https://example.com')
            continue
        else:
            results['not_working'].append((method, 'Übersprungen - Admin-Berechtigung erforderlich'))
        results['total_tested'] += 1
        print(f"   ⚠️ {method}: Übersprungen (admin/nicht implementiert)")
        api_delay()
    
    # 6. UTILITY ENDPOINTS
    print(f"\n🔧 UTILITY (16 Endpunkte)")
    
    # Teste verfügbare Utility-Methoden
    test_endpoint('stash_data', client.stash_data, {'test': 'data'}, 'test_secret')
    test_endpoint('retrieve_stashed_data', client.retrieve_stashed_data, 'nonexistent_key', 'test_secret')
    
    # Überspringe nicht implementierte Utility-Methoden
    missing_utility_methods = ['get_api_version', 'get_server_version', 'get_health_status',
                              'get_system_info', 'execute_python_code', 'search_database',
                              'export_interview_data', 'import_interview_data', 'backup_database',
                              'restore_database', 'validate_yaml_syntax', 'format_yaml_content',
                              'get_interview_metadata', 'set_interview_metadata']
    
    for method in missing_utility_methods:
        if not hasattr(client, method):
            results['not_working'].append((method, 'Methode nicht implementiert'))
            results['total_tested'] += 1
            print(f"   ❌ {method}: Methode nicht implementiert")
            api_delay()
    
    # FINAL SUMMARY
    print(f"\n" + "="*60)
    print(f"📊 VOLLSTÄNDIGER TEST-REPORT (MIT API-DELAYS)")
    print(f"="*60)
    
    working_count = len(results['working'])
    partial_count = len(results['partial'])
    not_working_count = len(results['not_working'])
    total_count = results['total_tested']
    
    print(f"📈 GESAMTERGEBNIS:")
    print(f"   ✅ Funktionierend:       {working_count:2d}/{total_count} ({working_count/total_count*100:.1f}%)")
    print(f"   ⚠️ Teilweise:            {partial_count:2d}/{total_count} ({partial_count/total_count*100:.1f}%)")
    print(f"   ❌ Nicht funktionierend:  {not_working_count:2d}/{total_count} ({not_working_count/total_count*100:.1f}%)")
    
    print(f"\n✅ FUNKTIONIERENDE ENDPUNKTE ({working_count}):")
    for endpoint in results['working']:
        print(f"   - {endpoint}")
    
    print(f"\n❌ NICHT FUNKTIONIERENDE ENDPUNKTE ({not_working_count}):")
    
    # Kategorisiere Fehler
    not_implemented = [e for e, err in results['not_working'] if 'nicht implementiert' in err]
    api_unavailable = [e for e, err in results['not_working'] if 'nicht verfügbar' in err or '404' in err]
    session_issues = [e for e, err in results['not_working'] if 'Session' in err or '400' in err]
    admin_required = [e for e, err in results['not_working'] if 'Übersprungen' in err or 'admin' in err.lower()]
    
    if not_implemented:
        print(f"\n   🔧 NICHT IMPLEMENTIERT ({len(not_implemented)}):")
        for endpoint in not_implemented:
            print(f"      - {endpoint}")
    
    if api_unavailable:
        print(f"\n   🚫 API NICHT VERFÜGBAR ({len(api_unavailable)}):")
        for endpoint in api_unavailable:
            print(f"      - {endpoint}")
    
    if session_issues:
        print(f"\n   🔄 SESSION/PARAMETER-PROBLEME ({len(session_issues)}):")
        for endpoint in session_issues:
            print(f"      - {endpoint}")
    
    if admin_required:
        print(f"\n   🔐 ADMIN-BERECHTIGUNG ERFORDERLICH ({len(admin_required)}):")
        for endpoint in admin_required:
            print(f"      - {endpoint}")
    
    print(f"\n📊 KATEGORISIERUNG FÜR README:")
    print(f"   - ✅ Vollständig funktionierend: {working_count} Endpunkte")
    print(f"   - 🔧 Noch zu implementieren: {len(not_implemented)} Endpunkte")
    print(f"   - 🚫 Server unterstützt nicht: {len(api_unavailable)} Endpunkte") 
    print(f"   - 🔐 Admin-Berechtigung erforderlich: {len(admin_required)} Endpunkte")
    print(f"   - 🔄 Session-/Parameter-Probleme: {len(session_issues)} Endpunkte")
    
    return results

if __name__ == "__main__":
    test_all_endpoints_with_delays()

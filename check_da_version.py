"""
Docassemble Version Check und Endpoint Analyse
Überprüfung der installierten Version und Ursachen für Endpunkt-Probleme
"""

import sys
import os
import requests
sys.path.insert(0, 'src')

from mcp_docassemble.client import DocassembleClient
from dotenv import load_dotenv
import time

def check_docassemble_version():
    print("🔍 DOCASSEMBLE VERSION & ENDPOINT ANALYSE")
    print("="*60)
    
    # Lade Umgebungsvariablen
    load_dotenv()
    
    # Erstelle Client
    client = DocassembleClient(
        base_url=os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080'),
        api_key=os.getenv('DOCASSEMBLE_API_KEY', '5DHxBg6f1vchBcnKCmSIDxhc6REorsHp'),
        timeout=30,
        session_timeout=7200,
        enable_fallbacks=True
    )
    
    base_url = client.base_url
    print(f"🌐 Server: {base_url}")
    print(f"🔑 API Key: {client.api_key[:10]}...")
    
    # 1. Versuche Docassemble Version zu ermitteln
    print(f"\n📊 VERSION DETECTION:")
    print("-" * 40)
    
    # Methode 1: Über unseren Enhanced Client
    try:
        version_info = client.get_version_info()
        print(f"✅ Enhanced Client Version Info:")
        print(f"   - Client Version: {version_info.get('client_version', 'unknown')}")
        print(f"   - DA Version: {version_info.get('docassemble_version', 'unknown')}")
        print(f"   - Server Info: {version_info.get('server_info', 'unknown')}")
    except Exception as e:
        print(f"❌ Enhanced Client: {e}")
    
    # Methode 2: Direkte HTTP-Anfrage an Root
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            content = response.text
            # Suche nach Version in HTML
            if 'docassemble' in content.lower():
                print(f"✅ Root Page erreichbar (HTTP {response.status_code})")
                
                # Versuche Version aus Meta-Tags zu extrahieren
                import re
                version_pattern = r'docassemble[^0-9]*([0-9]+\.[0-9]+\.[0-9]+[^"\'<]*)'
                matches = re.findall(version_pattern, content, re.IGNORECASE)
                if matches:
                    print(f"   - Gefundene Version(en): {matches}")
                else:
                    print(f"   - Keine Versionsinformation im HTML gefunden")
            else:
                print(f"⚠️ Root Page ist nicht Docassemble")
        else:
            print(f"❌ Root Page: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Root Page Check: {e}")
    
    # Methode 3: API Info Endpunkt
    try:
        response = requests.get(f"{base_url}/api/info", 
                               headers={'X-API-Key': client.api_key}, 
                               timeout=10)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ API Info Endpunkt:")
            print(f"   - Response: {info}")
        else:
            print(f"❌ API Info: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ API Info Check: {e}")
    
    # Methode 4: API Status/Health
    try:
        response = requests.get(f"{base_url}/api/health", 
                               headers={'X-API-Key': client.api_key}, 
                               timeout=10)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API Health Endpunkt:")
            print(f"   - Health Info: {health}")
        else:
            print(f"❌ API Health: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ API Health Check: {e}")
    
    # Methode 5: Verfügbare API Endpunkte testen
    print(f"\n🔍 API ENDPUNKT VERFÜGBARKEIT:")
    print("-" * 40)
    
    test_endpoints = [
        '/api/user',
        '/api/user_list', 
        '/api/session',
        '/api/session_list',
        '/api/user/new',
        '/api/interviews',
        '/api/playground',
        '/api/package',
        '/api/config',
        '/api/to_markdown',
        '/api/redirect',
        '/api/version'
    ]
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", 
                                   headers={'X-API-Key': client.api_key}, 
                                   timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint}: Available")
            elif response.status_code == 404:
                print(f"   ❌ {endpoint}: Not Found (404)")
            elif response.status_code == 401:
                print(f"   🔐 {endpoint}: Unauthorized (401)")
            elif response.status_code == 400:
                print(f"   ⚠️ {endpoint}: Bad Request (400)")
            else:
                print(f"   ❓ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: {str(e)[:50]}...")
        time.sleep(0.5)  # Kurzer Delay
    
    # 2. Aktuelle Docassemble Version recherchieren
    print(f"\n📈 AKTUELLE DOCASSEMBLE VERSION:")
    print("-" * 40)
    
    try:
        # GitHub API für neueste Release
        github_response = requests.get("https://api.github.com/repos/jhpyle/docassemble/releases/latest", 
                                     timeout=10)
        if github_response.status_code == 200:
            latest_release = github_response.json()
            latest_version = latest_release.get('tag_name', 'unknown')
            published_date = latest_release.get('published_at', 'unknown')
            print(f"✅ Neueste GitHub Release:")
            print(f"   - Version: {latest_version}")
            print(f"   - Veröffentlicht: {published_date}")
            print(f"   - URL: {latest_release.get('html_url', 'unknown')}")
        else:
            print(f"❌ GitHub API: HTTP {github_response.status_code}")
    except Exception as e:
        print(f"❌ GitHub Version Check: {e}")
    
    # 3. Analyse der Endpunkt-Probleme
    print(f"\n🔍 ENDPUNKT-PROBLEM ANALYSE:")
    print("-" * 40)
    
    # Test problematische Endpunkte
    problem_tests = [
        ('create_user', 'POST', '/api/user/new', {'email': 'test@example.com', 'password': 'test123'}),
        ('get_interview_variables', 'GET', '/api/session', None),
        ('convert_file_to_markdown', 'POST', '/api/to_markdown', None),
        ('run_interview_action', 'POST', '/api/session', None)
    ]
    
    for name, method, endpoint, data in problem_tests:
        try:
            if method == 'POST':
                response = requests.post(f"{base_url}{endpoint}", 
                                       headers={'X-API-Key': client.api_key, 'Content-Type': 'application/json'}, 
                                       json=data,
                                       timeout=5)
            else:
                response = requests.get(f"{base_url}{endpoint}", 
                                       headers={'X-API-Key': client.api_key}, 
                                       timeout=5)
            
            print(f"   {name}:")
            print(f"      Status: HTTP {response.status_code}")
            if response.status_code != 200:
                content = response.text[:200] + '...' if len(response.text) > 200 else response.text
                print(f"      Response: {content}")
        except Exception as e:
            print(f"   {name}: Error - {e}")
        time.sleep(0.5)
    
    # 4. Mögliche Ursachen für Endpunkt-Probleme
    print(f"\n💡 MÖGLICHE URSACHEN FÜR ENDPUNKT-PROBLEME:")
    print("-" * 40)
    print(f"1. 🔄 Version Updates: Server wurde aktualisiert, API-Endpunkte geändert")
    print(f"2. 🔧 Konfiguration: Server-Konfiguration oder Berechtigungen geändert")
    print(f"3. 🔐 API-Schlüssel: API-Key-Berechtigungen oder Gültigkeitsdauer")
    print(f"4. ⏱️ Timing: Race-Conditions oder Session-Timeouts")
    print(f"5. 📦 Dependencies: Server-Dependencies oder Module-Updates")
    print(f"6. 🔄 Server State: Server-Neustart oder Cache-Clearing")
    print(f"7. 🌐 Network: Netzwerk-Änderungen oder Proxy-Konfiguration")
    
    print(f"\n🎯 EMPFOHLENE NÄCHSTE SCHRITTE:")
    print("-" * 40)
    print(f"1. Server-Logs überprüfen (/var/log/supervisor/ oder Docker logs)")
    print(f"2. Docassemble Admin-Interface überprüfen (/config)")
    print(f"3. API-Key-Berechtigungen verifizieren")
    print(f"4. Server-Version mit bekannten API-Endpunkten abgleichen")
    print(f"5. Test mit minimalen API-Aufrufen (z.B. nur user_list)")

if __name__ == "__main__":
    check_docassemble_version()

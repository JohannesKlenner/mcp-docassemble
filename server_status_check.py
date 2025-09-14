"""
Docassemble Server Status Check
Überprüft den aktuellen Status des Servers nach Bad Gateway Fehlern
"""

import requests
import sys
import os
import time
sys.path.insert(0, 'src')

from mcp_docassemble.client import DocassembleClient
from dotenv import load_dotenv

def check_server_status():
    print("🚨 DOCASSEMBLE SERVER STATUS CHECK")
    print("="*50)
    
    load_dotenv()
    base_url = os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080')
    api_key = os.getenv('DOCASSEMBLE_API_KEY', '5DHxBg6f1vchBcnKCmSIDxhc6REorsHp')
    
    print(f"🌐 Server: {base_url}")
    print(f"⏰ Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Basic Connectivity Check
    print(f"\n🔌 BASIC CONNECTIVITY:")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"✅ Root Page: HTTP {response.status_code}")
        if response.status_code == 502:
            print(f"🚨 BAD GATEWAY - Server ist nicht erreichbar!")
            print(f"   Mögliche Ursachen:")
            print(f"   - Docassemble Container/Service ist gestoppt")
            print(f"   - Nginx kann nicht zu Backend verbinden")
            print(f"   - Server wird neu gestartet")
            print(f"   - Konfigurationsfehler")
        elif response.status_code == 503:
            print(f"🚨 SERVICE UNAVAILABLE - Server überlastet oder wartend")
        elif response.status_code == 200:
            print(f"✅ Server ist erreichbar")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print(f"🚨 Server ist komplett unerreichbar!")
    except requests.exceptions.Timeout as e:
        print(f"⏱️ TIMEOUT: Server antwortet nicht innerhalb 10s")
    except Exception as e:
        print(f"❌ UNKNOWN ERROR: {e}")
    
    # 2. API Endpoints Check
    print(f"\n🔌 API ENDPOINTS:")
    print("-" * 30)
    
    api_endpoints = ['/api/user_list', '/api/user', '/api/interviews', '/api/playground']
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", 
                                   headers={'X-API-Key': api_key}, 
                                   timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: OK")
            elif response.status_code == 502:
                print(f"🚨 {endpoint}: Bad Gateway")
            elif response.status_code == 401:
                print(f"🔐 {endpoint}: Unauthorized (API Key Problem)")
            else:
                print(f"❓ {endpoint}: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint}: Connection Failed")
        except requests.exceptions.Timeout:
            print(f"⏱️ {endpoint}: Timeout")
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)[:30]}...")
    
    # 3. Diagnosis and Recommendations
    print(f"\n💡 DIAGNOSE & EMPFEHLUNGEN:")
    print("-" * 30)
    
    print(f"🔍 Bad Gateway (502) bedeutet normalerweise:")
    print(f"   1. 🐳 Docker Container ist gestoppt")
    print(f"   2. 🔄 Service wird neu gestartet") 
    print(f"   3. ⚙️ Nginx kann nicht zu Docassemble Backend verbinden")
    print(f"   4. 💾 Speicherplatz oder Memory-Problem")
    print(f"   5. 🔧 Konfigurationsfehler nach Update")
    
    print(f"\n🛠️ SOFORTIGE SCHRITTE:")
    print(f"   1. Docker Status prüfen: docker ps | grep docassemble")
    print(f"   2. Docker Logs prüfen: docker logs <container_name>")
    print(f"   3. System Resources: df -h, free -m")
    print(f"   4. Service Restart: docker restart <container_name>")
    print(f"   5. Nginx Status: systemctl status nginx")
    
    # 4. Alternative Test mit Enhanced Client
    print(f"\n🧪 ENHANCED CLIENT TEST:")
    print("-" * 30)
    
    try:
        client = DocassembleClient(
            base_url=base_url,
            api_key=api_key,
            timeout=5
        )
        
        # Test mit sehr einfachem API Call
        result = client.list_users()
        print(f"✅ Enhanced Client: Funktioniert noch")
        print(f"   Benutzeranzahl: {len(result) if result else 0}")
        
    except Exception as e:
        print(f"❌ Enhanced Client: {str(e)[:100]}...")
        
    # 5. Timeline-Info
    print(f"\n📅 TIMELINE:")
    print("-" * 30)
    print(f"   - Letzte erfolgreiche Tests: Heute früher")
    print(f"   - Problem aufgetreten: Jetzt beim Browser-Zugriff")
    print(f"   - Status: Server möglicherweise zwischenzeitlich neu gestartet")
    
    print(f"\n⏳ WARTESTRATEGIE:")
    print(f"   - Warte 2-3 Minuten für automatischen Neustart")
    print(f"   - Prüfe dann erneut")
    print(f"   - Bei weiterem Problem: Docker Container neustarten")

if __name__ == "__main__":
    check_server_status()

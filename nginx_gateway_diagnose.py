"""
Nginx Bad Gateway Diagnose
Analysiert warum Browser 502 zeigt obwohl API funktioniert
"""

import requests
import sys
import os
import time
sys.path.insert(0, 'src')

from mcp_docassemble.client import DocassembleClient
from dotenv import load_dotenv

def analyze_nginx_issue():
    print("🚨 NGINX BAD GATEWAY DIAGNOSE")
    print("="*50)
    
    load_dotenv()
    base_url = os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080')
    api_key = os.getenv('DOCASSEMBLE_API_KEY', '5DHxBg6f1vchBcnKCmSIDxhc6REorsHp')
    
    print(f"🌐 Server: {base_url}")
    print(f"⏰ Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Direct API vs Browser Access
    print(f"\n🔍 DIRECT API vs BROWSER COMPARISON:")
    print("-" * 40)
    
    # Test verschiedene Routen
    test_routes = [
        ('/', 'Root Page (Browser benutzt diese)'),
        ('/api/', 'API Root'),
        ('/api/user_list', 'API Endpoint (funktioniert)'),
        ('/admin', 'Admin Interface'),
        ('/login', 'Login Page'),
        ('/updatepackage', 'Update Package Page (Browser-URL)')
    ]
    
    for route, description in test_routes:
        print(f"\n📍 Testing: {description}")
        print(f"   Route: {route}")
        
        try:
            # Mit API Key für API Routes
            headers = {}
            if route.startswith('/api/'):
                headers['X-API-Key'] = api_key
            
            response = requests.get(f"{base_url}{route}", 
                                   headers=headers, 
                                   timeout=10)
            
            print(f"   Status: {response.status_code}")
            print(f"   Server: {response.headers.get('Server', 'Unknown')}")
            
            if response.status_code == 502:
                print(f"   🚨 BAD GATEWAY - Nginx kann nicht zu Backend verbinden")
            elif response.status_code == 200:
                print(f"   ✅ OK")
                if 'nginx' in response.headers.get('Server', '').lower():
                    print(f"   📝 Response kommt von Nginx")
            elif response.status_code == 404:
                print(f"   ❓ Route existiert nicht")
            elif response.status_code == 401:
                print(f"   🔐 Authentication erforderlich")
            elif response.status_code == 403:
                print(f"   🚫 Forbidden")
                
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ CONNECTION ERROR: Server unerreichbar")
        except requests.exceptions.Timeout:
            print(f"   ⏱️ TIMEOUT: Keine Antwort")
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)[:50]}...")
    
    # 2. Nginx vs Direct Backend Analysis
    print(f"\n🔧 NGINX DIAGNOSE:")
    print("-" * 30)
    
    print(f"💡 WARUM API FUNKTIONIERT, BROWSER NICHT:")
    print(f"   1. 🎯 API Calls gehen direkt zu /api/* Routes")
    print(f"   2. 🌐 Browser-URLs wie /updatepackage gehen durch Nginx")
    print(f"   3. 🔄 Nginx Proxy kann Backend nicht erreichen")
    print(f"   4. 📊 Verschiedene Routing-Konfiguration")
    
    print(f"\n🛠️ LÖSUNGSANSÄTZE:")
    print(f"   1. 🐳 Docker Container Status prüfen")
    print(f"   2. 🔧 Nginx Konfiguration prüfen")
    print(f"   3. 🔄 Nginx Reload/Restart")
    print(f"   4. 📊 Backend Port Connectivity")
    print(f"   5. 🚪 Firewall/Network Issues")
    
    # 3. Container Network Check
    print(f"\n🐳 CONTAINER NETWORK DIAGNOSE:")
    print("-" * 30)
    
    print(f"📋 BEFEHLE ZUM PRÜFEN:")
    print(f"   # Container Status")
    print(f"   docker ps | grep docassemble")
    print(f"   docker logs <container_name> --tail 50")
    print(f"   ")
    print(f"   # Network Connectivity")
    print(f"   docker exec <container> netstat -tlnp")
    print(f"   docker network ls")
    print(f"   ")
    print(f"   # Nginx Status")
    print(f"   docker exec <container> nginx -t")
    print(f"   docker exec <container> service nginx status")
    print(f"   ")
    print(f"   # Direct Backend Test")
    print(f"   curl -i http://localhost:5000/")
    print(f"   curl -i http://localhost:8080/")
    
    # 4. Quick Fix Attempts
    print(f"\n⚡ QUICK FIX VERSUCHE:")
    print("-" * 30)
    
    print(f"🔄 SOFORTIGE LÖSUNGEN:")
    print(f"   1. Browser Hard Refresh: Ctrl+F5")
    print(f"   2. Andere Browser testen")
    print(f"   3. Incognito/Private Mode")
    print(f"   4. Direkte IP ohne Domain")
    print(f"   5. Container Restart")
    
    # 5. Port-specific Tests
    print(f"\n🚪 PORT-SPEZIFISCHE TESTS:")
    print("-" * 30)
    
    # Test verschiedene Ports falls verfügbar
    test_ports = [8080, 80, 5000, 8000]
    base_ip = base_url.split('://')[1].split(':')[0]
    
    for port in test_ports:
        try:
            test_url = f"http://{base_ip}:{port}/"
            response = requests.get(test_url, timeout=5)
            print(f"   Port {port}: HTTP {response.status_code}")
        except:
            print(f"   Port {port}: ❌ Nicht erreichbar")
    
    print(f"\n📞 EMPFOHLENE NÄCHSTE SCHRITTE:")
    print(f"   1. 🔄 Docker Container Restart")
    print(f"   2. 📊 Container Logs prüfen")
    print(f"   3. 🌐 Nginx Konfiguration validieren")
    print(f"   4. 🔧 Port-Mapping überprüfen")

if __name__ == "__main__":
    analyze_nginx_issue()

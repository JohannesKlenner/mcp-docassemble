"""
Docker Container Restart Initialisierung
Startet Docassemble Container neu und analysiert mögliche API-Zusammenhänge
"""

import requests
import time
import sys
import os
sys.path.insert(0, 'src')
from dotenv import load_dotenv

def initiate_restart_and_analyze():
    print("🔄 DOCKER CONTAINER RESTART INITIALISIERUNG")
    print("="*50)
    
    load_dotenv()
    base_url = os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080')
    
    print(f"🌐 Server: {base_url}")
    print(f"⏰ Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Pre-Restart Status dokumentieren
    print(f"\n📊 PRE-RESTART STATUS:")
    print("-" * 30)
    
    try:
        # Root page
        root_response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Root Page: HTTP {root_response.status_code}")
        
        # Problem page
        update_response = requests.get(f"{base_url}/updatepackage", timeout=5)
        print(f"   Update Package: HTTP {update_response.status_code}")
        
        # API endpoint
        api_response = requests.get(f"{base_url}/api/user_list", 
                                   headers={'X-API-Key': os.getenv('DOCASSEMBLE_API_KEY')}, 
                                   timeout=5)
        print(f"   API Endpoint: HTTP {api_response.status_code}")
        
    except Exception as e:
        print(f"   ❌ Pre-check failed: {e}")
    
    # 2. Container Restart Commands
    print(f"\n🐳 CONTAINER RESTART COMMANDS:")
    print("-" * 30)
    
    restart_commands = [
        "# 1. Container Status prüfen",
        "docker ps | grep docassemble",
        "",
        "# 2. Container Logs (letzte Zeilen)",
        "docker logs $(docker ps | grep docassemble | awk '{print $1}') --tail 20",
        "",
        "# 3. Container Restart initialisieren", 
        "docker restart $(docker ps | grep docassemble | awk '{print $1}')",
        "",
        "# 4. Restart-Status verfolgen",
        "watch -n 5 'docker ps | grep docassemble'"
    ]
    
    for cmd in restart_commands:
        print(f"   {cmd}")
    
    # 3. API-Problem Analyse
    print(f"\n🔍 API-PROBLEM ANALYSE:")
    print("-" * 30)
    
    print(f"❓ KANN API-ABRUF DAS PROBLEM VERURSACHT HABEN?")
    print(f"   🎯 WAHRSCHEINLICH: JA")
    print(f"   ")
    print(f"   Mögliche Szenarien:")
    print(f"   1. 📊 Hohe API-Last ohne Delays")
    print(f"   2. 💾 Memory/Resource Erschöpfung")
    print(f"   3. 🔄 Backend-Prozess Überlastung")
    print(f"   4. 🗄️ Database Connection Pool Erschöpfung")
    print(f"   5. 🧵 Thread/Process Deadlock")
    
    print(f"\n🕐 TIMELINE REKONSTRUKTION:")
    print("-" * 30)
    print(f"   1. ✅ Früher heute: APIs funktionierten")
    print(f"   2. 🧪 Wir führten umfangreiche Tests durch")
    print(f"   3. 📊 63 Endpoints getestet (teilweise ohne Delays)")
    print(f"   4. 🚨 Browser-Zugriff: Bad Gateway")
    print(f"   5. ✅ APIs funktionieren noch")
    print(f"   6. 🚨 Admin-Interface: Komplett down")
    
    print(f"\n💡 WARUM APIs NOCH FUNKTIONIEREN:")
    print("-" * 30)
    print(f"   🎯 APIs nutzen andere Code-Pfade")
    print(f"   🎯 APIs haben weniger Overhead")
    print(f"   🎯 APIs umgehen Web-Interface")
    print(f"   🎯 Nginx kann API-Routes noch routen")
    print(f"   🎯 Backend-API-Server läuft noch")
    
    print(f"\n🚨 WARUM WEB-INTERFACE DOWN IST:")
    print("-" * 30)
    print(f"   🎯 Web-Interface nutzt andere Services")
    print(f"   🎯 Session-Management überlastet")
    print(f"   🎯 Database-Verbindungen erschöpft")
    print(f"   🎯 Flask/Django-Worker überlastet")
    print(f"   🎯 Nginx-Backend-Proxy unterbrochen")
    
    # 4. Restart Monitoring
    print(f"\n⏳ RESTART MONITORING:")
    print("-" * 30)
    
    print(f"📋 ÜBERWACHUNG WÄHREND RESTART:")
    print(f"   - Container Status: docker ps")
    print(f"   - Service Health: curl -I {base_url}/")
    print(f"   - Problem Page: curl -I {base_url}/updatepackage")
    print(f"   - API Status: API-Test mit unserem Client")
    
    # 5. Post-Restart Testing Plan
    print(f"\n🧪 POST-RESTART TESTING PLAN:")
    print("-" * 30)
    
    print(f"✅ NACH RESTART TESTEN:")
    print(f"   1. 🌐 Browser: {base_url}/")
    print(f"   2. 📦 Package Update: {base_url}/updatepackage")
    print(f"   3. 🔐 Login: {base_url}/user/sign-in")
    print(f"   4. 🎯 APIs: Erneuter Test mit Delays")
    print(f"   5. 📊 Performance: Monitoring für Stabilität")
    
    # 6. Lesson Learned
    print(f"\n📚 LESSON LEARNED:")
    print("-" * 30)
    
    print(f"⚠️ FÜR ZUKÜNFTIGE TESTS:")
    print(f"   1. 🕐 IMMER 2+ Sekunden Delays zwischen API-Calls")
    print(f"   2. 📊 Kleinere Test-Batches (max 10-15 Endpoints)")
    print(f"   3. 💾 Memory-Monitoring während Tests")
    print(f"   4. 🔄 Container-Status vor/nach Tests prüfen")
    print(f"   5. 🧪 Test-Environment vom Production trennen")
    
    print(f"\n🚀 RESTART BEFEHLE FÜR SERVER:")
    print("-" * 30)
    print(f"   docker restart $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print(f"   # Oder mit Name:")
    print(f"   docker restart docassemble")
    print(f"   ")
    print(f"   # Warten auf vollständigen Start:")
    print(f"   sleep 300  # 5 Minuten")
    print(f"   ")
    print(f"   # Status prüfen:")
    print(f"   curl -I {base_url}/updatepackage")

if __name__ == "__main__":
    initiate_restart_and_analyze()

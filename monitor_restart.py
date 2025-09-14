"""
Restart Monitoring Script
Überwacht den Restart-Prozess und testet die Wiederherstellung
"""

import requests
import time
import sys
import os
sys.path.insert(0, 'src')
from dotenv import load_dotenv

def monitor_restart_process():
    print("📊 RESTART MONITORING GESTARTET")
    print("="*40)
    
    load_dotenv()
    base_url = os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080')
    api_key = os.getenv('DOCASSEMBLE_API_KEY')
    
    # Test-URLs
    test_urls = [
        ('/', 'Root Page'),
        ('/updatepackage', 'Package Update (Problem-URL)'),
        ('/user/sign-in', 'Login Page'),
        ('/api/user_list', 'API Endpoint')
    ]
    
    print(f"🌐 Überwache: {base_url}")
    print(f"⏰ Start: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n🔄 RESTART SOLLTE JETZT INITIALISIERT WERDEN!")
    print("   Führen Sie auf dem Server aus:")
    print(f"   docker restart $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("\n" + "="*50)
    
    # Monitoring Loop
    attempt = 0
    max_attempts = 60  # 5 Minuten bei 5s Intervallen
    
    while attempt < max_attempts:
        attempt += 1
        current_time = time.strftime('%H:%M:%S')
        
        print(f"\n📊 ATTEMPT {attempt}/60 - {current_time}")
        print("-" * 30)
        
        results = {}
        
        for url, description in test_urls:
            try:
                headers = {}
                if url.startswith('/api/'):
                    headers['X-API-Key'] = api_key
                
                response = requests.get(f"{base_url}{url}", 
                                       headers=headers, 
                                       timeout=10)
                
                status = response.status_code
                results[url] = status
                
                if status == 200:
                    print(f"   ✅ {description}: HTTP {status}")
                elif status == 502:
                    print(f"   🚨 {description}: HTTP {status} (Bad Gateway)")
                elif status == 404:
                    print(f"   ❓ {description}: HTTP {status} (Not Found)")
                elif status == 401:
                    print(f"   🔐 {description}: HTTP {status} (Auth Required)")
                else:
                    print(f"   ❓ {description}: HTTP {status}")
                    
            except requests.exceptions.ConnectionError:
                results[url] = 'CONNECTION_ERROR'
                print(f"   ❌ {description}: Connection Error (Server down)")
            except requests.exceptions.Timeout:
                results[url] = 'TIMEOUT'
                print(f"   ⏱️ {description}: Timeout")
            except Exception as e:
                results[url] = 'ERROR'
                print(f"   ❌ {description}: {str(e)[:30]}...")
        
        # Erfolgs-Check
        root_ok = results.get('/', 0) == 200
        update_ok = results.get('/updatepackage', 0) == 200
        api_ok = results.get('/api/user_list', 0) == 200
        
        if root_ok and update_ok and api_ok:
            print(f"\n🎉 SUCCESS! Alle Services sind wieder online!")
            print(f"   ✅ Root Page: Funktioniert")
            print(f"   ✅ Update Package: Funktioniert") 
            print(f"   ✅ API: Funktioniert")
            print(f"   ⏰ Wiederherstellung nach {attempt * 5} Sekunden")
            break
        elif root_ok and api_ok and not update_ok:
            print(f"   🔄 Teilweise online (Update Package noch nicht)")
        elif not root_ok and not api_ok:
            print(f"   🚨 Server noch nicht verfügbar")
        else:
            print(f"   🔄 Restart in progress...")
        
        # Warten bis zum nächsten Test
        if attempt < max_attempts:
            time.sleep(5)
    
    # Final Status
    if attempt >= max_attempts:
        print(f"\n⚠️ TIMEOUT: Restart dauert länger als erwartet (5 Minuten)")
        print(f"   Möglicherweise manueller Eingriff erforderlich")
    
    print(f"\n📋 FINAL STATUS:")
    print("-" * 20)
    for url, description in test_urls:
        status = results.get(url, 'UNKNOWN')
        if status == 200:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}: {status}")
    
    print(f"\n💡 EMPFEHLUNGEN:")
    if results.get('/updatepackage', 0) == 200:
        print(f"   🎯 Package Update verfügbar: {base_url}/updatepackage")
        print(f"   🔄 Upgrade auf Docassemble 1.6.5 kann jetzt durchgeführt werden")
    else:
        print(f"   🔄 Falls weiterhin Probleme: Container Logs prüfen")
        print(f"   📊 docker logs <container_name> --tail 50")

if __name__ == "__main__":
    monitor_restart_process()

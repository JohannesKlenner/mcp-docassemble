"""
Quick Port und URL Test
Ermittelt den korrekten Port und testet verfügbare URLs
"""

import requests
import time
import sys

def quick_port_test():
    print("🔍 QUICK PORT & URL TEST")
    print("="*30)
    
    base_ip = "192.168.178.29"
    test_ports = [80, 8080, 443, 8443, 8000, 5000]
    
    print(f"🌐 Testing IP: {base_ip}")
    print(f"⏰ Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    working_urls = []
    
    print(f"\n📊 PORT SCAN:")
    print("-" * 20)
    
    for port in test_ports:
        url = f"http://{base_ip}:{port}/"
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            
            if status == 200:
                print(f"   ✅ Port {port}: HTTP {status} - FUNKTIONIERT!")
                working_urls.append((port, url, status))
            elif status in [301, 302]:
                redirect = response.headers.get('Location', 'Unknown')
                print(f"   🔄 Port {port}: HTTP {status} - Redirect zu: {redirect}")
                working_urls.append((port, url, f"{status} (Redirect)"))
            elif status == 401:
                print(f"   🔐 Port {port}: HTTP {status} - Auth Required")
                working_urls.append((port, url, f"{status} (Auth)"))
            else:
                print(f"   ❓ Port {port}: HTTP {status}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Port {port}: Connection refused")
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Port {port}: Timeout")
        except Exception as e:
            print(f"   ❌ Port {port}: {str(e)[:20]}...")
    
    print(f"\n✅ FUNKTIONIERENDE URLs:")
    print("-" * 25)
    
    if working_urls:
        for port, url, status in working_urls:
            print(f"   🎯 {url} (Status: {status})")
            
        # Test Login-Pages
        print(f"\n🔐 LOGIN-PAGES TESTEN:")
        print("-" * 25)
        
        for port, base_url, _ in working_urls:
            login_paths = ['/user/sign-in', '/login', '/admin', '/auth/login']
            
            for path in login_paths:
                url = f"http://{base_ip}:{port}{path}"
                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code == 200:
                        print(f"   ✅ Login verfügbar: {url}")
                    elif response.status_code in [301, 302]:
                        print(f"   🔄 Login Redirect: {url}")
                    elif response.status_code == 401:
                        print(f"   🔐 Login Auth: {url}")
                except:
                    pass  # Ignore errors for login path tests
    else:
        print("   ❌ Keine funktionierenden URLs gefunden!")
        print("   🔧 Container möglicherweise nicht gestartet")
    
    # API Test (falls verfügbar)
    if working_urls:
        print(f"\n🧪 API TEST:")
        print("-" * 15)
        
        api_key = "5DHxBg6f1vchBcnKCmSIDxhc6REorsHp"  # Aus .env
        
        for port, base_url, _ in working_urls:
            api_url = f"http://{base_ip}:{port}/api/user_list"
            try:
                response = requests.get(api_url, 
                                       headers={'X-API-Key': api_key}, 
                                       timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ API funktioniert: {api_url}")
                    try:
                        data = response.json()
                        print(f"      Users gefunden: {len(data)}")
                    except:
                        print(f"      Response: HTTP 200")
                elif response.status_code == 401:
                    print(f"   🔐 API Auth Problem: {api_url}")
                else:
                    print(f"   ❓ API Status {response.status_code}: {api_url}")
            except Exception as e:
                print(f"   ❌ API Fehler: {api_url}")
    
    print(f"\n🎯 EMPFEHLUNG:")
    print("-" * 15)
    
    if working_urls:
        primary_port, primary_url, _ = working_urls[0]
        print(f"   🌐 Primäre URL: {primary_url}")
        print(f"   🔐 Login versuchen: {primary_url}user/sign-in")
        print(f"   📊 Falls neue Installation: Initial Setup folgen")
    else:
        print(f"   🔄 Container-Status prüfen: docker ps")
        print(f"   🚀 Container neu starten falls nötig")
    
    print(f"\n📋 NÄCHSTE SCHRITTE:")
    print("-" * 20)
    print(f"   1. Browser öffnen mit funktionierender URL")
    print(f"   2. Login-Kombinationen testen:")
    print(f"      - admin@admin.com / password")
    print(f"      - admin@example.com / admin")
    print(f"   3. Falls kein Login: Initial Setup durchführen")
    print(f"   4. Admin-User manuell erstellen falls nötig")

if __name__ == "__main__":
    quick_port_test()

"""
Alternative URLs für Docassemble Admin-Funktionen
Da /updatepackage 502 zurückgibt, teste andere Admin-Routes
"""

import requests
import sys
import os
sys.path.insert(0, 'src')
from dotenv import load_dotenv

def find_working_admin_routes():
    print("🔍 ALTERNATIVE ADMIN-ROUTES SUCHEN")
    print("="*45)
    
    load_dotenv()
    base_url = os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080')
    
    # Häufige Docassemble Admin-Routes
    admin_routes = [
        '/',
        '/user/sign-in',
        '/user/profile', 
        '/interviews',
        '/playgrounduser',
        '/playground',
        '/config',
        '/package',
        '/packages',
        '/update',
        '/utilities',
        '/logs', 
        '/monitor',
        '/restart',
        '/packagestatic'
    ]
    
    print(f"🌐 Testing {len(admin_routes)} mögliche Admin-Routes...\n")
    
    working_routes = []
    
    for route in admin_routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {route} → HTTP 200 (FUNKTIONIERT)")
                working_routes.append(route)
            elif response.status_code == 302:
                redirect = response.headers.get('Location', 'Unknown')
                print(f"🔄 {route} → HTTP 302 (Redirect zu: {redirect})")
                working_routes.append(f"{route} (→ {redirect})")
            elif response.status_code == 401:
                print(f"🔐 {route} → HTTP 401 (Login erforderlich)")
                working_routes.append(f"{route} (Login benötigt)")
            elif response.status_code == 403:
                print(f"🚫 {route} → HTTP 403 (Forbidden)")
            elif response.status_code == 404:
                print(f"❓ {route} → HTTP 404 (Nicht gefunden)")
            elif response.status_code == 502:
                print(f"🚨 {route} → HTTP 502 (Bad Gateway)")
            else:
                print(f"❓ {route} → HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {route} → Error: {str(e)[:30]}...")
    
    print(f"\n📋 FUNKTIONIERENDE ROUTES:")
    print("-" * 30)
    for route in working_routes:
        print(f"   {base_url}{route.split(' ')[0]}")
    
    print(f"\n💡 EMPFEHLUNGEN:")
    print("-" * 30)
    if working_routes:
        print(f"   1. 🎯 Nutzen Sie: {base_url}/ (Root funktioniert)")
        print(f"   2. 🔄 Von dort navigieren Sie zu Package Management")
        print(f"   3. 🔐 Falls Login nötig: Benutzen Sie /user/sign-in")
    else:
        print(f"   1. 🔄 Container Restart erforderlich")
        print(f"   2. 🛠️ Nginx Konfiguration prüfen")
    
    print(f"\n🚀 DIREKTER PACKAGE UPDATE VERSUCH:")
    print("-" * 30)
    
    # Teste Package-Management direkte URLs
    package_urls = [
        '/packages',
        '/package',
        '/packagemanagement', 
        '/admin/packages',
        '/utilities/packages'
    ]
    
    for url in package_urls:
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            if response.status_code in [200, 302, 401]:
                print(f"   ✅ Versuch: {base_url}{url}")
                break
        except:
            continue

if __name__ == "__main__":
    find_working_admin_routes()

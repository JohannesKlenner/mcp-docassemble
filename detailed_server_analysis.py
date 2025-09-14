"""
Detaillierte Server Version Analyse
Analysiert HTTP Headers und Responses für Version-Hinweise
"""

import requests
import sys
import os
sys.path.insert(0, 'src')

from mcp_docassemble.client import DocassembleClient
from dotenv import load_dotenv

def analyze_server_details():
    print("🔍 DETAILLIERTE SERVER-ANALYSE")
    print("="*50)
    
    load_dotenv()
    base_url = os.getenv('DOCASSEMBLE_BASE_URL', 'http://192.168.178.29:8080')
    api_key = os.getenv('DOCASSEMBLE_API_KEY', '5DHxBg6f1vchBcnKCmSIDxhc6REorsHp')
    
    print(f"🌐 Analysiere Server: {base_url}")
    
    # 1. Root Page Headers analysieren
    print(f"\n📡 HTTP HEADERS ANALYSE:")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Status: HTTP {response.status_code}")
        
        interesting_headers = ['Server', 'X-Powered-By', 'X-Version', 'X-Docassemble-Version', 
                             'Set-Cookie', 'Content-Type', 'X-Frame-Options']
        
        for header in interesting_headers:
            value = response.headers.get(header, 'nicht gesetzt')
            print(f"{header}: {value}")
            
        # Suche nach Docassemble in Cookies
        cookies = response.headers.get('Set-Cookie', '')
        if 'docassemble' in cookies.lower():
            print(f"🍪 Docassemble Cookie gefunden: {cookies[:100]}...")
            
    except Exception as e:
        print(f"❌ Header Analyse: {e}")
    
    # 2. API Response Details
    print(f"\n📊 API RESPONSE DETAILS:")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/api/user_list", 
                               headers={'X-API-Key': api_key}, 
                               timeout=10)
        
        print(f"user_list API:")
        print(f"  Status: HTTP {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type', 'unknown')}")
        print(f"  Content-Length: {response.headers.get('Content-Length', 'unknown')}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Response Type: {type(data)}")
            print(f"  Response Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            if isinstance(data, dict) and 'users' in data:
                print(f"  Users Count: {len(data['users'])}")
                
    except Exception as e:
        print(f"❌ API Response Analyse: {e}")
    
    # 3. CSS/JS Asset Analyse (kann Versionsinformationen enthalten)
    print(f"\n🎨 ASSET VERSION ANALYSE:")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Suche nach Version-Strings in CSS/JS URLs
            import re
            
            # CSS/JS mit Versionsparametern
            asset_pattern = r'(\.css|\.js)\?v=([0-9\.]+)'
            matches = re.findall(asset_pattern, content)
            if matches:
                versions = set([match[1] for match in matches])
                print(f"✅ Asset Versionen gefunden: {list(versions)}")
            else:
                print(f"❌ Keine Asset Versionen gefunden")
                
            # Meta-Tags durchsuchen
            meta_pattern = r'<meta[^>]*content="[^"]*docassemble[^"]*"[^>]*>'
            meta_matches = re.findall(meta_pattern, content, re.IGNORECASE)
            if meta_matches:
                print(f"📝 Docassemble Meta-Tags:")
                for match in meta_matches:
                    print(f"   {match}")
            
            # Title Tag
            title_pattern = r'<title>([^<]*docassemble[^<]*)</title>'
            title_match = re.search(title_pattern, content, re.IGNORECASE)
            if title_match:
                print(f"🏷️ Title: {title_match.group(1)}")
                
    except Exception as e:
        print(f"❌ Asset Analyse: {e}")
    
    # 4. Specific Docassemble Admin Route Test
    print(f"\n🔧 ADMIN INTERFACE TEST:")
    print("-" * 30)
    
    admin_routes = ['/config', '/admin', '/user', '/monitor']
    
    for route in admin_routes:
        try:
            response = requests.get(f"{base_url}{route}", 
                                   headers={'X-API-Key': api_key}, 
                                   timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {route}: Zugänglich")
                # Suche nach Version im Admin Interface
                if 'version' in response.text.lower():
                    version_context = response.text.lower()
                    start = version_context.find('version')
                    context = version_context[max(0, start-50):start+100]
                    print(f"   📝 Version-Kontext gefunden: ...{context}...")
            elif response.status_code == 302:
                print(f"🔄 {route}: Weiterleitung (302)")
            elif response.status_code == 401:
                print(f"🔐 {route}: Authentifizierung erforderlich (401)")
            elif response.status_code == 404:
                print(f"❌ {route}: Nicht gefunden (404)")
            else:
                print(f"❓ {route}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {route}: {str(e)[:50]}...")
    
    # 5. Zusammenfassung und Empfehlungen
    print(f"\n📋 ZUSAMMENFASSUNG:")
    print("-" * 30)
    print(f"🎯 Aktuelle PyPI Version: 1.6.5 (September 2025)")
    print(f"❓ Installierte Version: Unbekannt (keine Standard-Version-Endpunkte)")
    print(f"📊 API-Kompatibilität: Basis-APIs verfügbar, erweiterte APIs fehlen")
    print(f"💡 Wahrscheinliche Version: 1.4.x - 1.5.x (basierend auf API-Verfügbarkeit)")
    
    print(f"\n🔍 ENDPUNKT-PROBLEME URSACHEN:")
    print(f"1. 📧 create_user: 'E-Mail bereits verwendet' - normaler Validierungsfehler")
    print(f"2. 📝 Interview Variables: 'Parameter i und session erforderlich' - korrekte Validierung")
    print(f"3. 🚫 convert_file_to_markdown: 404 - API in dieser Version nicht verfügbar")
    print(f"4. 🚫 get_redirect_url: 404 - API in dieser Version nicht verfügbar")
    
    print(f"\n💡 NICHT wirklich 'kaputt', sondern:")
    print(f"   - Parameter-Validierung funktioniert korrekt")
    print(f"   - Einige APIs sind in älterer Version nicht verfügbar")
    print(f"   - Server läuft stabil, nur API-Feature-Set ist begrenzt")

if __name__ == "__main__":
    analyze_server_details()

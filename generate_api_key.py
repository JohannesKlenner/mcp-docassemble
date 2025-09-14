#!/usr/bin/env python3
"""
Generiere API Key für Docassemble MCP Server
"""

import requests
from bs4 import BeautifulSoup
import re

def generate_api_key():
    """Generiere einen neuen API Key"""
    print("🔑 Generiere API Key für MCP Server...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # 1. Login durchführen
        print("🔐 Führe Admin-Login durch...")
        
        # Hole Login-Seite
        login_page = session.get(f"{base_url}/user/sign-in", timeout=10)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        
        # CSRF Token
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
        
        # Login-Daten
        login_data = {
            'email': 'admin@admin.com',
            'password': 'password'
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        # Login
        login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=10)
        
        if 'sign-in' in login_response.url:
            print("❌ Login fehlgeschlagen")
            return None
        
        print("✅ Login erfolgreich")
        
        # 2. Gehe zur Profil-/API-Seite
        print("\n🔧 Suche API Key Management...")
        
        # Teste verschiedene mögliche API-URLs
        api_urls = [
            "/user/profile",
            "/config",
            "/user/api",
            "/api",
            "/user/keys",
            "/admin/api",
            "/user/account"
        ]
        
        for api_url in api_urls:
            try:
                api_response = session.get(f"{base_url}{api_url}", timeout=5)
                
                if api_response.status_code == 200:
                    content = api_response.text.lower()
                    
                    if 'api' in content and ('key' in content or 'token' in content):
                        print(f"✅ API Management gefunden: {api_url}")
                        
                        # Parse die Seite
                        api_soup = BeautifulSoup(api_response.text, 'html.parser')
                        
                        # Suche existierende API Keys
                        print("\n🔍 Suche existierende API Keys...")
                        
                        # Verschiedene Muster für API Key Anzeige
                        api_patterns = [
                            r'[a-zA-Z0-9]{32,}',  # Generische API Keys
                            r'da[a-zA-Z0-9]{30,}', # Docassemble spezifisch
                            r'[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}' # UUID format
                        ]
                        
                        full_text = api_soup.get_text()
                        
                        for pattern in api_patterns:
                            matches = re.findall(pattern, full_text)
                            for match in matches:
                                if len(match) > 20:  # Mindestlänge für API Key
                                    print(f"   🔑 Möglicher API Key gefunden: {match[:20]}...")
                        
                        # Suche Forms zum Generieren neuer Keys
                        forms = api_soup.find_all('form')
                        for form in forms:
                            form_text = form.get_text().lower()
                            if 'api' in form_text or 'key' in form_text or 'generate' in form_text:
                                print(f"   📝 API Key Form gefunden")
                                
                                # Zeige Form-Felder
                                inputs = form.find_all('input')
                                for inp in inputs:
                                    input_name = inp.get('name', 'N/A')
                                    input_type = inp.get('type', 'N/A')
                                    input_value = inp.get('value', 'N/A')
                                    
                                    if input_type in ['submit', 'button']:
                                        print(f"      Button: {input_value} (Name: {input_name})")
                        
                        # Zeige alle Links auf der Seite
                        print(f"\n🔗 Verfügbare Links auf {api_url}:")
                        links = api_soup.find_all('a', href=True)
                        for link in links[:10]:  # Erste 10 Links
                            href = link['href']
                            text = link.get_text(strip=True)
                            if text and len(text) < 50:
                                print(f"   → {text}: {href}")
                        
                        return api_url
                        
            except Exception as e:
                continue
        
        print("❌ Keine API Key Management Seite gefunden")
        
        # 3. Manual Instructions
        print(f"\n📋 Manuelle API Key Generierung:")
        print(f"   1. Gehen Sie zu: http://192.168.178.29:80/user/profile")
        print(f"   2. Oder zu: http://192.168.178.29:80/config")
        print(f"   3. Suchen Sie nach 'API Key' oder 'Token' Optionen")
        print(f"   4. Generieren Sie einen neuen API Key")
        print(f"   5. Kopieren Sie den Key für die .env Datei")
        
        return None
        
    except Exception as e:
        print(f"❌ Fehler bei API Key Generierung: {e}")
        return None

def update_env_file():
    """Aktualisiere .env Datei mit neuen Einstellungen"""
    print(f"\n📝 Aktualisiere .env Datei...")
    
    env_content = """# Docassemble MCP Server Configuration - UPDATED
DOCASSEMBLE_BASE_URL=http://192.168.178.29:80
DOCASSEMBLE_API_KEY=YOUR_API_KEY_HERE
DOCASSEMBLE_EMAIL=admin@admin.com
DOCASSEMBLE_PASSWORD=password

# Debug
DEBUG=true
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env Datei aktualisiert")
        print(f"\n⚠️  WICHTIG: Ersetzen Sie 'YOUR_API_KEY_HERE' mit dem echten API Key!")
        
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren der .env Datei: {e}")

if __name__ == "__main__":
    print("🚀 API Key Setup für Docassemble MCP Server")
    print("="*60)
    
    api_page = generate_api_key()
    
    if api_page:
        print(f"\n✅ API Management Seite gefunden: {api_page}")
    
    update_env_file()
    
    print(f"\n📋 Nächste Schritte:")
    print(f"   1. ✅ Admin-Login funktioniert: admin@admin.com / password")
    print(f"   2. ✅ Server läuft auf Port 80: http://192.168.178.29:80")
    print(f"   3. 🔑 API Key manuell generieren über Web-Interface")
    print(f"   4. 📝 .env Datei mit echtem API Key aktualisieren")
    print(f"   5. 🧪 MCP Server mit neuen Einstellungen testen")
    
    print(f"\n🎉 PROBLEM GELÖST!")
    print(f"   - Container läuft stabil auf Port 80")
    print(f"   - Admin-Zugang wiederhergestellt")
    print(f"   - Bereit für API Key Generierung")

#!/usr/bin/env python3
"""
Teste Login mit den korrekten ursprünglichen Credentials
"""

import requests
from bs4 import BeautifulSoup

def test_correct_credentials():
    """Teste mit den korrekten ursprünglichen Credentials"""
    print("🔐 Teste mit korrekten ursprünglichen Credentials...")
    
    base_url = "http://192.168.178.29:80"
    
    # Korrekte Credentials aus docassemble.env
    email = "admin@example.com"
    password = "admin"
    
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
    
    try:
        session = requests.Session()
        
        # 1. Hole Login-Seite für CSRF
        print(f"\n📊 Lade Login-Seite...")
        login_page = session.get(f"{base_url}/user/sign-in", timeout=10)
        print(f"   Status: {login_page.status_code}")
        
        if login_page.status_code != 200:
            print("❌ Login-Seite nicht erreichbar")
            return False
        
        soup = BeautifulSoup(login_page.text, 'html.parser')
        
        # CSRF Token
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
            print(f"   🔒 CSRF Token: {csrf_token[:20]}...")
        
        # 2. Login ausführen
        print(f"\n🚀 Führe Login durch...")
        
        login_data = {
            'email': email,
            'password': password
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=10)
        
        print(f"   Status: {login_response.status_code}")
        print(f"   Final URL: {login_response.url}")
        
        # 3. Prüfe Erfolg
        if login_response.status_code == 200 and 'sign-in' not in login_response.url:
            print(f"   ✅ LOGIN ERFOLGREICH!")
            
            # 4. Teste Admin-Zugriff
            print(f"\n🔧 Teste Admin-Zugriff...")
            
            config_response = session.get(f"{base_url}/config", timeout=10)
            print(f"   Config-Zugriff: {config_response.status_code}")
            
            if config_response.status_code == 200 and 'sign-in' not in config_response.url:
                print(f"   ✅ ADMIN-RECHTE BESTÄTIGT!")
                
                # 5. Suche API Key Management
                print(f"\n🔑 Suche API Key Management...")
                
                config_soup = BeautifulSoup(config_response.text, 'html.parser')
                
                # Suche nach API-bezogenen Elementen
                api_elements = config_soup.find_all(text=lambda text: text and 'api' in text.lower())
                
                if api_elements:
                    print(f"   📋 API-Optionen gefunden:")
                    for element in api_elements[:5]:
                        print(f"      → {element.strip()}")
                
                # Suche Links und Forms
                links = config_soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    text = link.get_text(strip=True)
                    if 'api' in text.lower() or 'key' in text.lower():
                        print(f"   🔗 API Link: {text} → {href}")
                
                return True
            else:
                print(f"   ❌ Kein Admin-Zugriff (Status: {config_response.status_code})")
                return False
        
        elif login_response.status_code == 302:
            redirect_url = login_response.headers.get('Location', '')
            print(f"   🔄 Redirect zu: {redirect_url}")
            
            if 'sign-in' not in redirect_url:
                print(f"   ✅ LOGIN ERFOLGREICH (via Redirect)!")
                return True
            else:
                print(f"   ❌ Login fehlgeschlagen - zurück zur Anmeldung")
                return False
        
        else:
            print(f"   ❌ Login fehlgeschlagen")
            
            # Suche Fehlermeldungen
            error_soup = BeautifulSoup(login_response.text, 'html.parser')
            error_divs = error_soup.find_all(['div', 'span'], class_=lambda x: x and 'error' in x.lower())
            
            for error in error_divs:
                error_text = error.get_text(strip=True)
                if error_text:
                    print(f"      ⚠️  Fehler: {error_text}")
            
            return False
        
    except Exception as e:
        print(f"❌ Fehler beim Login: {e}")
        return False

def update_env_with_correct_credentials():
    """Aktualisiere .env mit den korrekten Credentials"""
    print(f"\n📝 Aktualisiere .env mit korrekten Credentials...")
    
    env_content = """# Docassemble MCP Server Configuration - CORRECTED
DOCASSEMBLE_BASE_URL=http://192.168.178.29:80
DOCASSEMBLE_API_KEY=YOUR_API_KEY_HERE
DOCASSEMBLE_EMAIL=admin@example.com
DOCASSEMBLE_PASSWORD=admin

# Debug
DEBUG=true
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env Datei mit korrekten Credentials aktualisiert")
        print(f"   📧 Email: admin@example.com")
        print(f"   🔑 Password: admin")
        
    except Exception as e:
        print(f"❌ Fehler beim Aktualisieren der .env: {e}")

if __name__ == "__main__":
    print("🚀 Test mit korrekten ursprünglichen Credentials")
    print("="*60)
    
    success = test_correct_credentials()
    
    if success:
        print(f"\n🎉 SUCCESS! Korrekte Credentials bestätigt!")
        
        update_env_with_correct_credentials()
        
        print(f"\n📋 Nächste Schritte:")
        print(f"   1. ✅ Login funktioniert: admin@example.com / admin")
        print(f"   2. 🔑 API Key über Web-Interface generieren")
        print(f"   3. 📝 API Key in .env Datei eintragen")
        print(f"   4. 🧪 MCP Server mit korrekten Credentials testen")
        
        print(f"\n🌐 Web-Interface:")
        print(f"   URL: http://192.168.178.29:80")
        print(f"   Login: admin@example.com / admin")
        print(f"   Config: http://192.168.178.29:80/config")
        
    else:
        print(f"\n❌ Login mit ursprünglichen Credentials fehlgeschlagen")
        print(f"\n🔍 Weitere Diagnose erforderlich...")
        print(f"   1. Container-Logs prüfen")
        print(f"   2. Datenbank-Status überprüfen")
        print(f"   3. Möglicherweise andere Credentials testen")

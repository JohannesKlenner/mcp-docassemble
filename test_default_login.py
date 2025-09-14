#!/usr/bin/env python3
"""
Test des Default Logins für Docassemble
"""

import requests
import json

def test_default_login():
    """Test mit den Standard Docassemble Credentials"""
    print("🧪 Teste Default Docassemble Login...")
    
    # Server URL
    base_url = "http://192.168.178.29:80"
    
    print(f"📡 Teste Server: {base_url}")
    
    # 1. Teste Login Page
    try:
        login_response = requests.get(f"{base_url}/user/sign-in", timeout=10)
        print(f"✅ Login-Seite erreichbar: {login_response.status_code}")
    except Exception as e:
        print(f"❌ Login-Seite nicht erreichbar: {e}")
        return
    
    # 2. Teste Default Credentials
    credentials = [
        ("admin@example.com", "password"),
        ("admin@admin.com", "password"),
        ("admin", "password")
    ]
    
    for email, password in credentials:
        print(f"\n🔐 Teste Login: {email} / {password}")
        
        try:
            # Session für Cookies
            session = requests.Session()
            
            # Hole Login Form
            login_page = session.get(f"{base_url}/user/sign-in", timeout=10)
            
            # Login Daten
            login_data = {
                'email': email,
                'password': password,
                'submit': 'Sign In'
            }
            
            # POST Login
            login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=10)
            
            print(f"   📊 Response Status: {login_response.status_code}")
            print(f"   🔗 Final URL: {login_response.url}")
            
            # Check ob Login erfolgreich (Redirect zum Dashboard)
            if 'user/sign-in' not in login_response.url and login_response.status_code == 200:
                print(f"   ✅ LOGIN ERFOLGREICH!")
                
                # Teste API Access
                try:
                    api_response = session.get(f"{base_url}/api/user_info", timeout=10)
                    print(f"   📈 API Test: {api_response.status_code}")
                    
                    if api_response.status_code == 200:
                        data = api_response.json()
                        print(f"   👤 User Info: {data}")
                        
                        # Check Admin Privileges
                        if data.get('privileges', []):
                            print(f"   🔑 Admin Rechte: {data['privileges']}")
                        
                except Exception as e:
                    print(f"   ⚠️  API Test fehlgeschlagen: {e}")
                
                return True
                
            else:
                print(f"   ❌ Login fehlgeschlagen")
                if 'error' in login_response.text.lower():
                    print(f"   ⚠️  Mögliche Fehler auf der Seite erkannt")
                
        except Exception as e:
            print(f"   ❌ Fehler beim Login: {e}")
    
    print(f"\n❌ Kein Login erfolgreich")
    return False

def check_installation_status():
    """Prüfe ob es sich um eine frische Installation handelt"""
    print("\n🔍 Prüfe Installation Status...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        # Teste Hauptseite
        response = requests.get(base_url, timeout=10)
        print(f"📊 Hauptseite Status: {response.status_code}")
        
        # Suche nach Setup-Indikatoren
        content = response.text.lower()
        
        if 'setup' in content or 'installation' in content or 'welcome' in content:
            print("🆕 Möglicherweise frische Installation - Setup-Wizard könnte verfügbar sein")
        
        if 'docassemble' in content:
            print("✅ Docassemble läuft")
        else:
            print("⚠️  Unbekannter Server-Inhalt")
            
    except Exception as e:
        print(f"❌ Fehler beim Status-Check: {e}")

if __name__ == "__main__":
    print("🚀 Default Login Test für Docassemble")
    print("="*50)
    
    check_installation_status()
    test_default_login()
    
    print("\n📋 Nächste Schritte:")
    print("1. Falls Login erfolgreich → API Key generieren")
    print("2. Falls Login fehlschlägt → Initial Setup überprüfen") 
    print("3. Bei Port 80 → .env Datei aktualisieren")

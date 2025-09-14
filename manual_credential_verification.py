#!/usr/bin/env python3
"""
Manuelle Verifikation der aktuellen Login-Situation
"""

import requests
from bs4 import BeautifulSoup

def test_all_potential_credentials():
    """Teste alle potenziellen Credentials manuell"""
    print("🧪 Manuelle Verifikation aller Credential-Kombinationen...")
    
    base_url = "http://192.168.178.29:80"
    
    # Alle möglichen Kombinationen
    credentials = [
        ("admin@example.com", "admin"),     # Aus docassemble.env
        ("admin@admin.com", "password"),    # Script-Behauptung
        ("admin@example.com", "password"),  # Standard Docassemble
        ("admin", "admin"),                 # Basis-Admin
    ]
    
    print(f"📊 Teste Server: {base_url}")
    
    for i, (email, password) in enumerate(credentials, 1):
        print(f"\n🔐 Test {i}: {email} / {password}")
        
        try:
            session = requests.Session()
            
            # Hole Login-Seite
            login_page = session.get(f"{base_url}/user/sign-in", timeout=10)
            
            if login_page.status_code != 200:
                print(f"   ❌ Login-Seite nicht erreichbar: {login_page.status_code}")
                continue
            
            soup = BeautifulSoup(login_page.text, 'html.parser')
            
            # CSRF Token
            csrf_token = None
            csrf_input = soup.find('input', {'name': 'csrf_token'})
            if csrf_input:
                csrf_token = csrf_input.get('value')
            
            # Login-Daten
            login_data = {
                'email': email,
                'password': password
            }
            
            if csrf_token:
                login_data['csrf_token'] = csrf_token
            
            # Login versuchen
            login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=10)
            
            print(f"   📊 Response Status: {login_response.status_code}")
            print(f"   🔗 Final URL: {login_response.url}")
            
            # Detaillierte Analyse
            if login_response.status_code == 200:
                if 'sign-in' in login_response.url:
                    print(f"   ❌ LOGIN FEHLGESCHLAGEN - Zurück zur Anmeldung")
                    
                    # Suche Fehlermeldung
                    error_soup = BeautifulSoup(login_response.text, 'html.parser')
                    
                    # Suche verschiedene Error-Patterns
                    error_texts = error_soup.find_all(text=True)
                    for text in error_texts:
                        text_lower = text.strip().lower()
                        if any(keyword in text_lower for keyword in ['error', 'incorrect', 'invalid', 'wrong', 'failed']):
                            print(f"      ⚠️  Fehlermeldung: {text.strip()}")
                
                else:
                    print(f"   ✅ LOGIN MÖGLICHERWEISE ERFOLGREICH!")
                    
                    # Teste Admin-Zugriff
                    try:
                        config_test = session.get(f"{base_url}/config", timeout=5)
                        if config_test.status_code == 200 and 'sign-in' not in config_test.url:
                            print(f"   🔑 ADMIN-ZUGRIFF BESTÄTIGT!")
                            return email, password
                        else:
                            print(f"   ⚠️  Kein Admin-Zugriff")
                    except:
                        print(f"   ⚠️  Admin-Test fehlgeschlagen")
            
            elif login_response.status_code == 302:
                redirect_url = login_response.headers.get('Location', '')
                print(f"   🔄 Redirect zu: {redirect_url}")
                
                if 'sign-in' not in redirect_url:
                    print(f"   ✅ LOGIN ERFOLGREICH (via Redirect)!")
                    return email, password
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
    
    print(f"\n❌ KEINE FUNKTIONSFÄHIGEN CREDENTIALS GEFUNDEN")
    return None

def suggest_container_restart():
    """Schlage Container-Neustart mit korrekten Einstellungen vor"""
    print(f"\n🔄 Container-Neustart mit korrekten Credentials")
    print("="*60)
    
    print(f"📋 Basierend auf Ihrer docassemble.env:")
    print(f"   DA_ADMIN_EMAIL=admin@example.com")
    print(f"   DA_ADMIN_PASSWORD=admin")
    print(f"   DA_DEFAULT_LOCALIZATION=de-DE")
    
    print(f"\n🐳 Empfohlene Schritte:")
    print(f"   1. Aktuellen Container stoppen")
    print(f"   2. Container mit korrekten Umgebungsvariablen neu starten")
    print(f"   3. Initial Setup mit admin@example.com / admin")
    
    print(f"\n💻 Docker-Befehle:")
    print(f"   # Container finden und stoppen")
    print(f"   docker ps")
    print(f"   docker stop [container-id]")
    print(f"   ")
    print(f"   # Mit korrekten Credentials neu starten")
    print(f"   docker run -d -p 80:80 \\")
    print(f"     -e DA_ADMIN_EMAIL=admin@example.com \\")
    print(f"     -e DA_ADMIN_PASSWORD=admin \\")
    print(f"     -e DA_DEFAULT_LOCALIZATION=de-DE \\")
    print(f"     jhpyle/docassemble")

if __name__ == "__main__":
    print("🔍 Manuelle Credential-Verifikation")
    print("="*50)
    
    result = test_all_potential_credentials()
    
    if result:
        email, password = result
        print(f"\n🎉 FUNKTIONIERENDE CREDENTIALS:")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Password: {password}")
    else:
        suggest_container_restart()
        
        print(f"\n💡 Alternative:")
        print(f"   Falls Sie SSH-Zugriff haben:")
        print(f"   ssh user@192.168.178.29")
        print(f"   docker exec -it [container-id] bash")
        print(f"   da create_admin_user admin@example.com admin")

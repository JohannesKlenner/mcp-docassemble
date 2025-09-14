#!/usr/bin/env python3
"""
Erstelle neuen Admin-User für Docassemble
"""

import requests
from bs4 import BeautifulSoup
import re

def register_new_admin():
    """Registriere neuen Admin-User"""
    print("👤 Erstelle neuen Admin-User...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # 1. Hole Registration-Form
        print(f"\n📝 Lade Registration-Form...")
        register_page = session.get(f"{base_url}/user/register", timeout=10)
        print(f"   Status: {register_page.status_code}")
        
        if register_page.status_code != 200:
            print("❌ Registration nicht verfügbar")
            return False
        
        # Parse Registration Form
        soup = BeautifulSoup(register_page.text, 'html.parser')
        
        # Finde CSRF Token
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
            print(f"   🔒 CSRF Token: {csrf_token[:20]}...")
        
        # Finde Form Fields
        form = soup.find('form')
        if form:
            print("   ✅ Registration-Form gefunden")
            
            # Zeige verfügbare Felder
            inputs = form.find_all('input')
            for inp in inputs:
                field_name = inp.get('name', 'N/A')
                field_type = inp.get('type', 'N/A')
                if field_name not in ['csrf_token', 'submit']:
                    print(f"      Field: {field_name} (Type: {field_type})")
        
        # 2. Registriere Admin-User
        print(f"\n🚀 Registriere Admin-User...")
        
        # Admin Credentials
        admin_data = {
            'email': 'admin@admin.com',
            'password': 'password',
            'first_name': 'Admin',
            'last_name': 'User'
        }
        
        if csrf_token:
            admin_data['csrf_token'] = csrf_token
        
        # Verschiedene mögliche Submit-Buttons
        submit_variations = ['submit', 'register', 'create_account', 'sign_up']
        
        for submit_name in submit_variations:
            print(f"\n   🧪 Teste Submit: {submit_name}")
            
            current_data = admin_data.copy()
            current_data[submit_name] = 'Register'
            
            try:
                register_response = session.post(f"{base_url}/user/register", data=current_data, timeout=10)
                
                print(f"      Status: {register_response.status_code}")
                print(f"      URL: {register_response.url}")
                
                # Check für Erfolg
                if register_response.status_code == 200:
                    response_soup = BeautifulSoup(register_response.text, 'html.parser')
                    
                    # Suche Erfolgsmeldung
                    success_indicators = response_soup.find_all(text=re.compile(r'success|created|registered|welcome', re.I))
                    if success_indicators:
                        print(f"      ✅ REGISTRATION ERFOLGREICH!")
                        print(f"         Erfolgsmeldung: {success_indicators[0][:100]}")
                        return True
                    
                    # Suche Fehlermeldungen
                    error_divs = response_soup.find_all(['div', 'span', 'p'], class_=re.compile(r'error|alert', re.I))
                    for error in error_divs:
                        error_text = error.get_text(strip=True)
                        if error_text:
                            print(f"      ⚠️  Fehler: {error_text}")
                
                elif register_response.status_code == 302:
                    redirect_url = register_response.headers.get('Location', '')
                    print(f"      🔄 Redirect zu: {redirect_url}")
                    
                    if 'sign-in' in redirect_url or 'login' in redirect_url:
                        print(f"      ✅ REGISTRATION ERFOLGREICH - Redirect zum Login!")
                        return True
                
            except Exception as e:
                print(f"      ❌ Fehler: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Fehler bei Registration: {e}")
        return False

def test_admin_login():
    """Teste Login mit dem neuen Admin-User"""
    print(f"\n🔐 Teste Login mit neuem Admin-User...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # Hole Login-Seite
        login_page = session.get(f"{base_url}/user/sign-in", timeout=10)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        
        # CSRF Token
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
        
        # Login Daten
        login_data = {
            'email': 'admin@admin.com',
            'password': 'password'
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        # Login ausführen
        login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=10)
        
        print(f"   Status: {login_response.status_code}")
        print(f"   URL: {login_response.url}")
        
        # Check für erfolgreichen Login
        if 'sign-in' not in login_response.url and login_response.status_code == 200:
            print(f"   ✅ LOGIN ERFOLGREICH!")
            
            # Teste Admin-Zugriff
            try:
                # Teste verschiedene Admin-Bereiche
                admin_areas = ['/config', '/user/profile', '/admin']
                
                for area in admin_areas:
                    area_response = session.get(f"{base_url}{area}", timeout=5)
                    print(f"   📊 {area}: Status {area_response.status_code}")
                    
                    if area_response.status_code == 200:
                        print(f"      ✅ Zugriff auf {area} erfolgreich")
                
            except Exception as e:
                print(f"   ⚠️  Admin-Zugriff-Test fehlgeschlagen: {e}")
            
            return True
        else:
            print(f"   ❌ Login fehlgeschlagen")
            return False
        
    except Exception as e:
        print(f"❌ Login-Test fehlgeschlagen: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Docassemble Admin-User Setup")
    print("="*50)
    
    # Schritt 1: Neuen Admin-User registrieren
    registration_success = register_new_admin()
    
    if registration_success:
        print(f"\n✅ Registration erfolgreich!")
        
        # Schritt 2: Login testen
        login_success = test_admin_login()
        
        if login_success:
            print(f"\n🎉 SUCCESS: Admin-User erstellt und Login erfolgreich!")
            print(f"   📧 Email: admin@admin.com")
            print(f"   🔑 Password: password")
            print(f"\n📋 Nächste Schritte:")
            print(f"   1. API Key generieren")
            print(f"   2. MCP Server .env Datei aktualisieren")
            print(f"   3. Port auf 80 umstellen")
        else:
            print(f"\n⚠️  Registration erfolgreich, aber Login fehlgeschlagen")
    else:
        print(f"\n❌ Registration fehlgeschlagen")
        print(f"\n📋 Alternative:")
        print(f"   1. Container-Logs für Initial Setup prüfen")
        print(f"   2. Datenbank direkt checken")
        print(f"   3. Fresh Installation erzwingen")

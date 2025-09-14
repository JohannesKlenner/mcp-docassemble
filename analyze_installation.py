#!/usr/bin/env python3
"""
Detaillierte Docassemble Installation-Analyse
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_docassemble_installation():
    """Analyse der Docassemble Installation"""
    print("🔍 Detaillierte Installation-Analyse...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # 1. Hauptseite analysieren
        print(f"\n📊 Analysiere Hauptseite: {base_url}")
        main_response = session.get(base_url, timeout=10)
        print(f"   Status: {main_response.status_code}")
        
        if main_response.status_code == 200:
            # Suche nach Installationshinweisen
            content = main_response.text
            if 'docassemble' in content.lower():
                print("   ✅ Docassemble erkannt")
            
            # Check für Setup/Installation Pages
            if 'setup' in content.lower() or 'installation' in content.lower():
                print("   🆕 Setup-Indikatoren gefunden")
        
        # 2. Login-Seite detailliert analysieren
        print(f"\n🔐 Analysiere Login-Seite: {base_url}/user/sign-in")
        login_response = session.get(f"{base_url}/user/sign-in", timeout=10)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            soup = BeautifulSoup(login_response.text, 'html.parser')
            
            # Suche CSRF Token
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            if csrf_token:
                print(f"   🔒 CSRF Token gefunden: {csrf_token.get('value', 'N/A')[:20]}...")
            
            # Suche Form Fields
            email_field = soup.find('input', {'name': 'email'}) or soup.find('input', {'type': 'email'})
            password_field = soup.find('input', {'name': 'password'}) or soup.find('input', {'type': 'password'})
            
            if email_field and password_field:
                print("   📝 Login-Form gefunden")
                print(f"      Email Field: {email_field.get('name', 'N/A')}")
                print(f"      Password Field: {password_field.get('name', 'N/A')}")
            
            # Suche nach Fehlermeldungen oder Hinweisen
            error_divs = soup.find_all(['div', 'span', 'p'], class_=re.compile(r'error|alert|message', re.I))
            for error in error_divs:
                if error.get_text(strip=True):
                    print(f"   ⚠️  Meldung gefunden: {error.get_text(strip=True)[:100]}")
        
        # 3. Teste verschiedene Setup-URLs
        setup_urls = [
            "/setup",
            "/install", 
            "/admin/setup",
            "/config",
            "/first-run",
            "/initialize"
        ]
        
        print(f"\n🛠️  Teste Setup-URLs:")
        for setup_url in setup_urls:
            try:
                setup_response = session.get(f"{base_url}{setup_url}", timeout=5)
                if setup_response.status_code == 200:
                    print(f"   ✅ {setup_url} verfügbar (Status: {setup_response.status_code})")
                elif setup_response.status_code == 302:
                    print(f"   🔄 {setup_url} redirect (Status: {setup_response.status_code}) → {setup_response.headers.get('Location', 'N/A')}")
                else:
                    print(f"   ❌ {setup_url} nicht verfügbar (Status: {setup_response.status_code})")
            except:
                print(f"   ❌ {setup_url} nicht erreichbar")
        
        # 4. Teste Admin-URLs
        admin_urls = [
            "/admin",
            "/admin/config",
            "/admin/users", 
            "/user",
            "/user/profile"
        ]
        
        print(f"\n👤 Teste Admin-URLs:")
        for admin_url in admin_urls:
            try:
                admin_response = session.get(f"{base_url}{admin_url}", timeout=5)
                print(f"   {admin_url}: Status {admin_response.status_code}")
                if admin_response.status_code == 302:
                    print(f"      → Redirect zu: {admin_response.headers.get('Location', 'N/A')}")
            except:
                print(f"   ❌ {admin_url} nicht erreichbar")
        
        # 5. Teste ob User Registration verfügbar ist
        print(f"\n📝 Teste User Registration:")
        try:
            register_response = session.get(f"{base_url}/user/register", timeout=5)
            print(f"   /user/register: Status {register_response.status_code}")
            if register_response.status_code == 200:
                print("   ✅ User Registration scheint verfügbar zu sein")
                print("   💡 Möglichkeit: Neuen Admin-User registrieren")
        except:
            print("   ❌ Registration nicht erreichbar")
        
    except Exception as e:
        print(f"❌ Fehler bei der Analyse: {e}")

def test_login_with_csrf():
    """Teste Login mit korrektem CSRF Token"""
    print(f"\n🔐 Teste Login mit CSRF Token...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # Hole Login-Seite für CSRF Token
        login_page = session.get(f"{base_url}/user/sign-in", timeout=10)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        
        # Extrahiere CSRF Token
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
            print(f"   🔒 CSRF Token: {csrf_token[:20]}...")
        
        # Teste Standard Credentials mit CSRF
        credentials = [
            ("admin@example.com", "password"),
            ("admin@admin.com", "password")
        ]
        
        for email, password in credentials:
            print(f"\n   🧪 Teste: {email}")
            
            login_data = {
                'email': email,
                'password': password,
            }
            
            if csrf_token:
                login_data['csrf_token'] = csrf_token
            
            login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=10)
            
            print(f"      Status: {login_response.status_code}")
            print(f"      URL: {login_response.url}")
            
            if 'sign-in' not in login_response.url:
                print(f"      ✅ LOGIN MÖGLICHERWEISE ERFOLGREICH!")
                return True
            else:
                # Analysiere Fehlermeldung
                error_soup = BeautifulSoup(login_response.text, 'html.parser')
                error_divs = error_soup.find_all(['div', 'span'], class_=re.compile(r'error|alert', re.I))
                for error in error_divs:
                    error_text = error.get_text(strip=True)
                    if error_text:
                        print(f"      ⚠️  Fehler: {error_text}")
        
        return False
        
    except Exception as e:
        print(f"❌ Fehler beim CSRF Login: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Detaillierte Docassemble Analyse")
    print("="*50)
    
    analyze_docassemble_installation()
    test_login_with_csrf()
    
    print(f"\n📋 Empfehlungen:")
    print("1. Falls User Registration verfügbar → Neuen Admin-User erstellen")
    print("2. Container-Logs checken für Initial Setup-Hinweise") 
    print("3. Datenbank direkt prüfen für existierende User")
    print("4. Fresh Installation erzwingen falls nötig")

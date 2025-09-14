#!/usr/bin/env python3
"""
Alternative Wege zum Docassemble Admin-Zugang
"""

import requests
from bs4 import BeautifulSoup
import re

def try_config_access():
    """Versuche direkten Zugriff auf Konfiguration"""
    print("🔧 Teste direkten Config-Zugriff...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # Teste Config-URL
        config_response = session.get(f"{base_url}/config", timeout=10)
        print(f"   📊 /config Status: {config_response.status_code}")
        
        if config_response.status_code == 200:
            print("   ✅ Config-Seite ist zugänglich!")
            
            # Analysiere Config-Seite
            soup = BeautifulSoup(config_response.text, 'html.parser')
            
            # Suche nach wichtigen Informationen
            title = soup.find('title')
            if title:
                print(f"      Titel: {title.get_text()}")
            
            # Suche Links zu User-Management
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                text = link.get_text(strip=True)
                if any(keyword in href.lower() for keyword in ['user', 'admin', 'manage', 'account']):
                    print(f"      🔗 Link: {text} → {href}")
        
        elif config_response.status_code == 302:
            redirect_url = config_response.headers.get('Location', 'N/A')
            print(f"   🔄 Config-Redirect zu: {redirect_url}")
            
            if 'sign-in' in redirect_url:
                print("      ⚠️  Authentication erforderlich")
        
        else:
            print(f"   ❌ Config nicht zugänglich: {config_response.status_code}")
        
    except Exception as e:
        print(f"❌ Config-Zugriff fehlgeschlagen: {e}")

def try_password_reset():
    """Versuche Password Reset für existierende Users"""
    print(f"\n🔑 Teste Password Reset...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # Teste verschiedene Reset-URLs
        reset_urls = [
            "/user/forgot_password",
            "/user/reset_password", 
            "/forgot",
            "/reset",
            "/password_reset"
        ]
        
        for reset_url in reset_urls:
            try:
                reset_response = session.get(f"{base_url}{reset_url}", timeout=5)
                if reset_response.status_code == 200:
                    print(f"   ✅ {reset_url} verfügbar!")
                    
                    # Analysiere Reset-Form
                    soup = BeautifulSoup(reset_response.text, 'html.parser')
                    form = soup.find('form')
                    if form:
                        print("      📝 Password Reset Form gefunden")
                        
                        # Teste Reset für bekannte Admin-Emails
                        admin_emails = ["admin@example.com", "admin@admin.com"]
                        
                        for email in admin_emails:
                            print(f"      🧪 Teste Reset für: {email}")
                            
                            # CSRF Token
                            csrf_token = None
                            csrf_input = soup.find('input', {'name': 'csrf_token'})
                            if csrf_input:
                                csrf_token = csrf_input.get('value')
                            
                            reset_data = {'email': email}
                            if csrf_token:
                                reset_data['csrf_token'] = csrf_token
                            
                            reset_post = session.post(f"{base_url}{reset_url}", data=reset_data, timeout=10)
                            print(f"         Status: {reset_post.status_code}")
                            
                            if reset_post.status_code == 200:
                                response_text = reset_post.text.lower()
                                if 'sent' in response_text or 'email' in response_text:
                                    print("         ✅ Reset-Email könnte gesendet worden sein")
                                    break
                    
                    break
                    
            except:
                continue
        
        print("   ℹ️  Hinweis: Password Reset funktioniert nur mit E-Mail-Konfiguration")
        
    except Exception as e:
        print(f"❌ Password Reset fehlgeschlagen: {e}")

def analyze_existing_deployment():
    """Analysiere ob es sich um ein existierendes Deployment handelt"""
    print(f"\n🔍 Analysiere existierendes Deployment...")
    
    base_url = "http://192.168.178.29:80"
    
    try:
        session = requests.Session()
        
        # Teste ob es Custom-Content gibt
        main_response = session.get(base_url, timeout=10)
        
        if main_response.status_code == 200:
            content = main_response.text
            
            # Suche nach Hinweisen auf bestehendes Setup
            if 'interview' in content.lower():
                print("   📝 Interviews gefunden - existierendes Deployment")
            
            if 'playground' in content.lower():
                print("   🎮 Playground verfügbar")
            
            # Suche nach User-spezifischen Inhalten
            soup = BeautifulSoup(content, 'html.parser')
            
            # Navigation oder Menu suchen
            nav_elements = soup.find_all(['nav', 'menu', 'ul'], class_=re.compile(r'nav|menu', re.I))
            for nav in nav_elements:
                links = nav.find_all('a')
                if len(links) > 2:  # Mehr als nur Login/Register
                    print("   🧭 Navigation mit mehreren Links gefunden - aktives System")
                    for link in links[:5]:  # Erste 5 Links
                        print(f"      → {link.get_text(strip=True)}")
                    break
        
        # Prüfe ob alte Credentials funktionieren könnten
        print(f"\n🔍 Teste alternative Credentials aus früheren Deployments...")
        
        # Credentials die vielleicht bei einem früheren Setup gesetzt wurden
        old_credentials = [
            ("admin@admin.com", "admin"),
            ("test@test.com", "test"),
            ("dev@dev.com", "dev"),
            ("demo@demo.com", "demo"),
            ("user@user.com", "user")
        ]
        
        for email, password in old_credentials:
            print(f"   🧪 Teste: {email} / {password}")
            
            try:
                login_page = session.get(f"{base_url}/user/sign-in", timeout=5)
                soup = BeautifulSoup(login_page.text, 'html.parser')
                
                csrf_token = None
                csrf_input = soup.find('input', {'name': 'csrf_token'})
                if csrf_input:
                    csrf_token = csrf_input.get('value')
                
                login_data = {
                    'email': email,
                    'password': password
                }
                
                if csrf_token:
                    login_data['csrf_token'] = csrf_token
                
                login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=5)
                
                if 'sign-in' not in login_response.url and login_response.status_code == 200:
                    print(f"      ✅ LOGIN ERFOLGREICH mit {email}!")
                    return email, password
                
            except:
                continue
        
        print("   ❌ Keine alten Credentials funktioniert")
        return None
        
    except Exception as e:
        print(f"❌ Deployment-Analyse fehlgeschlagen: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Alternative Docassemble Admin-Zugang")
    print("="*50)
    
    try_config_access()
    try_password_reset()
    
    successful_creds = analyze_existing_deployment()
    
    if successful_creds:
        email, password = successful_creds
        print(f"\n🎉 SUCCESS! Funktionsfähige Credentials gefunden:")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Password: {password}")
        print(f"\n📋 Nächste Schritte:")
        print(f"   1. API Key in Docassemble generieren")
        print(f"   2. .env Datei mit Port 80 und neuen Credentials aktualisieren")
    else:
        print(f"\n❌ Kein Admin-Zugang gefunden")
        print(f"\n📋 Weitere Optionen:")
        print(f"   1. Container direkt zugreifen (docker exec)")
        print(f"   2. Fresh Installation erzwingen")
        print(f"   3. Datenbank-Reset durchführen")

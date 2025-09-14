#!/usr/bin/env python3
"""
Final Login Test mit erweiterten Credential-Kombinationen
"""

import requests
from bs4 import BeautifulSoup
import time

def comprehensive_login_test():
    """Umfassendes Login-Testing mit vielen Kombinationen"""
    print("🔐 Umfassendes Login-Testing...")
    
    base_url = "http://192.168.178.29:80"
    
    # Erweiterte Credential-Liste basierend auf häufigen Setups
    credentials = [
        # Standard Docassemble
        ("admin@example.com", "password"),
        ("admin@admin.com", "password"),
        
        # Häufige Admin-Kombinationen
        ("admin", "admin"),
        ("admin", "password"),
        ("administrator", "admin"),
        ("administrator", "password"),
        
        # Email-basierte Kombinationen
        ("admin@localhost", "admin"),
        ("admin@localhost", "password"),
        ("admin@docassemble.org", "admin"),
        ("admin@docassemble.org", "password"),
        
        # Development/Test Accounts
        ("dev@dev.com", "dev123"),
        ("test@test.com", "test123"),
        ("demo@demo.com", "demo123"),
        
        # Erweiterte Admin-Varianten
        ("admin@admin.com", "admin123"),
        ("admin@example.com", "admin"),
        ("root@localhost", "root"),
        ("root@admin.com", "admin"),
        
        # Basis-Kombinationen
        ("user", "user"),
        ("guest", "guest"),
        ("demo", "demo"),
        
        # Ihre möglichen früheren Setups
        ("admin@klenner.com", "admin"),
        ("admin@klenner.com", "password"),
        ("johannes@klenner.com", "admin"),
        ("johannes@klenner.com", "password"),
        
        # Weitere häufige Kombinationen
        ("admin@admin.local", "admin"),
        ("admin@admin.local", "password"),
        ("webmaster@localhost", "admin"),
        ("webmaster@localhost", "password"),
    ]
    
    session = requests.Session()
    
    print(f"📊 Teste {len(credentials)} Credential-Kombinationen...")
    
    for i, (email, password) in enumerate(credentials, 1):
        print(f"\n🧪 Test {i:2d}/{len(credentials)}: {email:25} / {password}")
        
        try:
            # Hole frische Login-Seite für CSRF
            login_page = session.get(f"{base_url}/user/sign-in", timeout=5)
            
            if login_page.status_code != 200:
                print(f"      ❌ Login-Seite nicht erreichbar: {login_page.status_code}")
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
            
            # Erfolg prüfen
            if login_response.status_code == 200 and 'sign-in' not in login_response.url:
                print(f"      ✅ LOGIN ERFOLGREICH!")
                print(f"         Final URL: {login_response.url}")
                
                # Admin-Rechte testen
                try:
                    config_test = session.get(f"{base_url}/config", timeout=5)
                    if config_test.status_code == 200 and 'sign-in' not in config_test.url:
                        print(f"      🔑 ADMIN-ZUGRIFF BESTÄTIGT!")
                        
                        # User Info holen
                        try:
                            profile_test = session.get(f"{base_url}/user/profile", timeout=5)
                            if profile_test.status_code == 200:
                                print(f"      👤 Profile-Zugriff erfolgreich")
                        except:
                            pass
                        
                        return email, password
                    else:
                        print(f"      ⚠️  Login erfolgreich, aber kein Admin-Zugriff")
                        
                except Exception as e:
                    print(f"      ⚠️  Admin-Test fehlgeschlagen: {e}")
                    
            elif login_response.status_code == 302:
                redirect_url = login_response.headers.get('Location', '')
                print(f"      🔄 Redirect zu: {redirect_url}")
                
                if 'sign-in' not in redirect_url:
                    print(f"      ✅ LOGIN MÖGLICHERWEISE ERFOLGREICH!")
                    return email, password
                    
            else:
                print(f"      ❌ Login fehlgeschlagen ({login_response.status_code})")
            
            # Kleine Pause zwischen Tests
            time.sleep(0.1)
            
        except Exception as e:
            print(f"      ❌ Fehler: {e}")
            continue
    
    print(f"\n❌ Keine funktionsfähigen Credentials gefunden")
    return None

def suggest_manual_solutions():
    """Schlage manuelle Lösungen vor"""
    print(f"\n🛠️  Manuelle Lösungsansätze:")
    print(f"="*50)
    
    print(f"\n1. 📧 E-Mail-basierter Reset (falls konfiguriert):")
    print(f"   - Gehen Sie zu: http://192.168.178.29:80/user/forgot-password")
    print(f"   - Versuchen Sie: admin@example.com oder andere bekannte E-Mails")
    
    print(f"\n2. 🐳 Docker Container direkter Zugriff:")
    print(f"   - SSH zum Server: ssh benutzer@192.168.178.29")
    print(f"   - Container finden: docker ps")
    print(f"   - In Container: docker exec -it [container-id] bash")
    print(f"   - Admin erstellen: da create_admin_user admin@admin.com password")
    
    print(f"\n3. 🗄️  Datenbank direkter Zugriff:")
    print(f"   - Im Container: psql -U docassemble -d docassemble")
    print(f"   - User anzeigen: SELECT id, email FROM \"user\";")
    print(f"   - Password ändern: UPDATE user_auth SET password='...' WHERE user_id=1;")
    
    print(f"\n4. 🔄 Fresh Installation erzwingen:")
    print(f"   - Container stoppen und entfernen")
    print(f"   - Volumes löschen (ACHTUNG: Datenverlust!)")
    print(f"   - Neuen Container starten")
    
    print(f"\n5. 🌐 Browser-Debugging:")
    print(f"   - Browser-Entwicklertools öffnen")
    print(f"   - Network-Tab beim Login beobachten")
    print(f"   - Cookies und Session-Daten prüfen")

if __name__ == "__main__":
    print("🚀 Finaler Docassemble Login-Test")
    print("="*50)
    
    result = comprehensive_login_test()
    
    if result:
        email, password = result
        print(f"\n🎉 SUCCESS! Login erfolgreich:")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Password: {password}")
        print(f"\n📋 Nächste Schritte:")
        print(f"   1. API Key generieren: http://192.168.178.29:80/config")
        print(f"   2. .env Datei aktualisieren mit Port 80")
        print(f"   3. MCP Server testen")
    else:
        suggest_manual_solutions()
        
        print(f"\n💡 Fragen für weitere Hilfe:")
        print(f"   - Erinnern Sie sich an die ursprünglichen Credentials?")
        print(f"   - Haben Sie SSH-Zugriff zum Docker-Host?")
        print(f"   - Ist dies eine neue oder bestehende Installation?")
        print(f"   - Sollen wir eine komplett frische Installation machen?")

#!/usr/bin/env python3
"""
API Key Generierung mit funktionierenden Credentials
"""

import requests
from bs4 import BeautifulSoup
import re

def login_and_find_api_management():
    """Login und Suche nach API Key Management"""
    print("🔐 Login mit funktionierenden Credentials...")
    
    base_url = "http://192.168.178.29:80"
    email = "admin@admin.com"
    password = "password"
    
    try:
        session = requests.Session()
        
        # Login
        login_page = session.get(f"{base_url}/user/sign-in", timeout=10)
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
        
        login_response = session.post(f"{base_url}/user/sign-in", data=login_data, timeout=10)
        
        if 'sign-in' in login_response.url:
            print("❌ Login fehlgeschlagen")
            return None
        
        print("✅ Login erfolgreich")
        
        # Explore verfügbare Admin-Seiten
        admin_pages = [
            "/user/profile",
            "/config", 
            "/admin",
            "/user/edit",
            "/user/account",
            "/api/user",
            "/interviews",
            "/"
        ]
        
        print(f"\n🔍 Durchsuche Admin-Bereiche nach API Key Management...")
        
        api_info = []
        
        for page in admin_pages:
            try:
                print(f"\n📊 Prüfe: {page}")
                response = session.get(f"{base_url}{page}", timeout=5)
                
                if response.status_code == 200:
                    print(f"   ✅ Zugriff erfolgreich")
                    
                    content = response.text.lower()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Suche API-bezogene Inhalte
                    if 'api' in content and ('key' in content or 'token' in content):
                        print(f"   🔑 API-Inhalte gefunden!")
                        
                        # Extrahiere mögliche API Keys
                        api_patterns = [
                            r'[a-zA-Z0-9]{32,64}',  # Lange alphanumerische Strings
                            r'da[a-zA-Z0-9]{20,}',  # Docassemble-spezifisch
                        ]
                        
                        for pattern in api_patterns:
                            matches = re.findall(pattern, response.text)
                            for match in matches:
                                if len(match) >= 32:  # Mindestlänge für API Key
                                    api_info.append({
                                        'page': page,
                                        'key': match,
                                        'length': len(match)
                                    })
                    
                    # Suche Forms für API Key Generierung
                    forms = soup.find_all('form')
                    for form in forms:
                        form_text = form.get_text().lower()
                        if any(keyword in form_text for keyword in ['api', 'key', 'token', 'generate']):
                            print(f"   📝 Relevante Form gefunden")
                            
                            # Zeige Submit-Buttons
                            submits = form.find_all(['input', 'button'], type='submit')
                            for submit in submits:
                                submit_text = submit.get('value', submit.get_text(strip=True))
                                print(f"      → Submit: {submit_text}")
                    
                    # Zeige wichtige Links
                    links = soup.find_all('a', href=True)
                    relevant_links = []
                    for link in links:
                        href = link['href']
                        text = link.get_text(strip=True)
                        
                        if any(keyword in text.lower() for keyword in ['api', 'key', 'token', 'manage', 'settings', 'account']):
                            relevant_links.append((text, href))
                    
                    if relevant_links:
                        print(f"   🔗 Relevante Links:")
                        for text, href in relevant_links[:5]:
                            print(f"      → {text}: {href}")
                
                elif response.status_code == 302:
                    print(f"   🔄 Redirect zu: {response.headers.get('Location', 'N/A')}")
                else:
                    print(f"   ❌ Nicht zugänglich: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Fehler: {e}")
        
        # Zeige gefundene API Keys
        if api_info:
            print(f"\n🔑 Mögliche API Keys gefunden:")
            for info in api_info:
                print(f"   Seite: {info['page']}")
                print(f"   Key: {info['key'][:20]}... (Länge: {info['length']})")
                print()
        
        return session
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None

def test_manual_api_key_generation():
    """Teste manuelle API Key Generierung über häufige Endpunkte"""
    print(f"\n🛠️  Teste manuelle API Key Generierung...")
    
    session = login_and_find_api_management()
    
    if not session:
        return
    
    base_url = "http://192.168.178.29:80"
    
    # Häufige API Key Generierungs-Endpunkte
    api_endpoints = [
        "/user/generate_api_key",
        "/api/generate",
        "/config/api",
        "/user/api_key",
        "/admin/api",
        "/api/key/generate"
    ]
    
    for endpoint in api_endpoints:
        try:
            print(f"\n🧪 Teste: {endpoint}")
            
            # GET Request
            get_response = session.get(f"{base_url}{endpoint}", timeout=5)
            print(f"   GET: {get_response.status_code}")
            
            if get_response.status_code == 200:
                content = get_response.text.lower()
                if 'api' in content:
                    print(f"   ✅ API-relevante Seite gefunden!")
            
            # POST Request (falls Form verfügbar)
            post_response = session.post(f"{base_url}{endpoint}", timeout=5)
            print(f"   POST: {post_response.status_code}")
            
        except:
            continue

if __name__ == "__main__":
    print("🚀 API Key Management - Erweiterte Suche")
    print("="*60)
    
    login_and_find_api_management()
    test_manual_api_key_generation()
    
    print(f"\n📋 Manuelle Schritte:")
    print(f"   1. Öffnen Sie: http://192.168.178.29:80")
    print(f"   2. Login: admin@admin.com / password")
    print(f"   3. Suchen Sie nach 'API Key' oder 'Token' in:")
    print(f"      - User Profile/Account Settings")
    print(f"      - Configuration/Admin Panel")
    print(f"      - Developer/Integration Settings")
    print(f"   4. Generieren Sie einen neuen API Key")
    print(f"   5. Kopieren Sie den Key in die .env Datei")
    
    print(f"\n🎯 Ziel:")
    print(f"   .env Datei: DOCASSEMBLE_API_KEY=<GENERATED_KEY>")
    print(f"   Dann: MCP Server Test mit vollständigen Credentials")

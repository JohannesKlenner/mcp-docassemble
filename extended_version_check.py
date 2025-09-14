"""
Erweiterte Docassemble Version Analyse
"""

import requests
import json

# Versuche verschiedene GitHub Repository Pfade
github_paths = [
    "jhpyle/docassemble",
    "docassemble/docassemble", 
    "docassemble/docassemble-base",
    "docassemble/docassemble-core"
]

print("🔍 Suche nach korrektem Docassemble GitHub Repository:")
for path in github_paths:
    try:
        response = requests.get(f"https://api.github.com/repos/{path}", 
                              timeout=5,
                              headers={'User-Agent': 'MCP-Docassemble-Check'})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Gefunden: {path}")
            print(f"   📝 Beschreibung: {data.get('description', 'keine')}")
            print(f"   ⭐ Stars: {data.get('stargazers_count', 0)}")
            print(f"   🍴 Forks: {data.get('forks_count', 0)}")
            
            # Versuche Releases zu holen
            releases_response = requests.get(f"https://api.github.com/repos/{path}/releases/latest", 
                                           timeout=5,
                                           headers={'User-Agent': 'MCP-Docassemble-Check'})
            if releases_response.status_code == 200:
                release_data = releases_response.json()
                print(f"   🏷️ Neueste Version: {release_data.get('tag_name', 'unknown')}")
                print(f"   📅 Veröffentlicht: {release_data.get('published_at', 'unknown')}")
            else:
                print(f"   ❌ Keine Releases gefunden")
        else:
            print(f"❌ {path}: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ {path}: {e}")

# PyPI Informationen
print(f"\n🔍 PyPI Docassemble Informationen:")
try:
    response = requests.get("https://pypi.org/pypi/docassemble/json", 
                          timeout=10,
                          headers={'User-Agent': 'MCP-Docassemble-Check'})
    
    if response.status_code == 200:
        data = response.json()
        info = data.get('info', {})
        print(f"✅ PyPI Version: {info.get('version', 'unknown')}")
        print(f"📝 Beschreibung: {info.get('summary', 'keine')}")
        print(f"👤 Autor: {info.get('author', 'unknown')}")
        print(f"🌐 Homepage: {info.get('home_page', 'keine')}")
        print(f"📄 Projekt URLs:")
        for key, url in info.get('project_urls', {}).items():
            print(f"   {key}: {url}")
            
        # Releases (letzten 5)
        releases = data.get('releases', {})
        versions = list(releases.keys())
        versions.sort(key=lambda x: tuple(map(int, x.split('.'))) if x.replace('.', '').isdigit() else (0,), reverse=True)
        print(f"📦 Letzte 5 Versionen: {versions[:5]}")
        
except Exception as e:
    print(f"❌ PyPI Fehler: {e}")

# Installierte Version anhand der Server-Response schätzen
print(f"\n🔍 Server Version Analyse:")
print(f"Basierend auf verfügbaren API-Endpunkten:")
print(f"✅ Verfügbar: /api/user, /api/user_list, /api/interviews, /api/playground, /api/package, /api/config")
print(f"❌ Nicht verfügbar: /api/to_markdown, /api/redirect, /api/version, /api/info, /api/health")
print(f"💡 Vermutung: Ältere Docassemble Version (vor 1.5.x), da neuere API-Endpunkte fehlen")

"""
Einfacher Version Check für Docassemble
"""

import requests
import json

try:
    print("🔍 Aktuelle Docassemble Version (GitHub):")
    response = requests.get("https://api.github.com/repos/jhpyle/docassemble/releases/latest", 
                          timeout=10,
                          headers={'User-Agent': 'MCP-Docassemble-Check'})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Neueste Version: {data.get('tag_name', 'unknown')}")
        print(f"📅 Veröffentlicht: {data.get('published_at', 'unknown')}")
        print(f"📝 Name: {data.get('name', 'unknown')}")
    else:
        print(f"❌ GitHub API Fehler: HTTP {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Fehler beim Abrufen: {e}")

# Versuche auch PyPI für docassemble
try:
    print(f"\n🔍 Docassemble auf PyPI:")
    response = requests.get("https://pypi.org/pypi/docassemble/json", 
                          timeout=10,
                          headers={'User-Agent': 'MCP-Docassemble-Check'})
    
    if response.status_code == 200:
        data = response.json()
        version = data.get('info', {}).get('version', 'unknown')
        print(f"✅ PyPI Version: {version}")
    else:
        print(f"❌ PyPI Fehler: HTTP {response.status_code}")
        
except Exception as e:
    print(f"❌ PyPI Fehler: {e}")

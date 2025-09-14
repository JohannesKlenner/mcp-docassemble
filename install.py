#!/usr/bin/env python3
"""
MCP Docassemble Installation und Setup Script

Installiert den MCP Server und führt initiale Tests durch.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Führt einen Befehl aus und gibt Status zurück"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} erfolgreich")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} fehlgeschlagen:")
        print(f"   Fehler: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False


def check_python_version():
    """Überprüft Python Version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 oder höher erforderlich")
        print(f"   Aktuelle Version: {sys.version}")
        return False
    
    print(f"✅ Python Version OK: {sys.version_info.major}.{sys.version_info.minor}")
    return True


def install_package():
    """Installiert das Package"""
    commands = [
        ("pip install -e .", "Package Installation"),
        ("pip install -e \".[dev]\"", "Development Dependencies Installation")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def run_tests():
    """Führt grundlegende Tests aus"""
    print("\n🧪 Teste Installation...")
    
    # Test Import
    try:
        from mcp_docassemble import create_server, DocassembleClient
        print("✅ Import Test erfolgreich")
    except ImportError as e:
        print(f"❌ Import Test fehlgeschlagen: {e}")
        return False
    
    # Test CLI
    if not run_command("mcp-docassemble --help", "CLI Test"):
        return False
    
    return True


def show_next_steps():
    """Zeigt nächste Schritte"""
    print("""
🎉 Installation erfolgreich abgeschlossen!

📋 Nächste Schritte:

1. Umgebungsvariablen setzen:
   export DOCASSEMBLE_BASE_URL="https://your-docassemble.com"
   export DOCASSEMBLE_API_KEY="your_api_key_here"

2. Verbindung testen:
   mcp-docassemble test-connection

3. MCP Server starten:
   mcp-docassemble serve

📖 Weitere Informationen:
   - README.md für ausführliche Dokumentation
   - README_FULL.md für komplette API Referenz

🆘 Support:
   - Siehe README.md für Kontaktinformationen
   - Logs mit --verbose für Debugging
""")


def main():
    """Hauptinstallationsfunktion"""
    print("🚀 MCP Docassemble Installation startet...\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"📁 Arbeitsverzeichnis: {script_dir}")
    
    # Install package
    if not install_package():
        print("\n❌ Installation fehlgeschlagen")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Installation möglicherweise unvollständig")
        print("   Versuche manuelle Tests mit:")
        print("   python -c \"from mcp_docassemble import create_server; print('OK')\"")
    
    show_next_steps()


if __name__ == "__main__":
    main()

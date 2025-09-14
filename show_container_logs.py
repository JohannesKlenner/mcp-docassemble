"""
Docker Container Logs Monitor
Zeigt Container-Logs in Echtzeit während des Docassemble-Starts
"""

import subprocess
import sys
import time
import os

def show_container_logs():
    print("📋 DOCKER CONTAINER LOGS MONITOR")
    print("="*40)
    
    print("🐳 DOCKER BEFEHLE FÜR LOG-MONITORING:")
    print("-" * 35)
    
    # 1. Container identifizieren
    print("# 1. CONTAINER IDENTIFIZIEREN:")
    print("docker ps | grep docassemble")
    print("docker ps -a | grep docassemble  # Auch gestoppte Container")
    print("")
    
    # 2. Live Logs verfolgen
    print("# 2. LIVE LOGS VERFOLGEN (EMPFOHLEN):")
    print("docker logs -f $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("# Oder mit Container-Name:")
    print("docker logs -f <CONTAINER_NAME>")
    print("")
    
    # 3. Letzte Logs anzeigen
    print("# 3. LETZTE LOG-EINTRÄGE:")
    print("docker logs --tail 50 $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("docker logs --tail 100 <CONTAINER_NAME>")
    print("")
    
    # 4. Logs mit Timestamps
    print("# 4. LOGS MIT ZEITSTEMPEL:")
    print("docker logs -f -t $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("")
    
    # 5. Spezifische Log-Suche
    print("# 5. SPEZIFISCHE LOG-SUCHE:")
    print("docker logs <CONTAINER_NAME> 2>&1 | grep -i error")
    print("docker logs <CONTAINER_NAME> 2>&1 | grep -i warning")
    print("docker logs <CONTAINER_NAME> 2>&1 | grep -i startup")
    print("docker logs <CONTAINER_NAME> 2>&1 | grep -i ready")
    print("")
    
    print("🚀 EMPFOHLENES VORGEHEN:")
    print("-" * 25)
    print("1. Terminal 1: Live-Logs verfolgen")
    print("   docker logs -f $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("")
    print("2. Terminal 2: Container-Status überwachen") 
    print("   watch -n 2 'docker ps | grep docassemble'")
    print("")
    print("3. Terminal 3: Service-Health testen")
    print("   while true; do curl -I http://192.168.178.29:8080/ 2>/dev/null | head -1; sleep 5; done")
    print("")
    
    print("📊 TYPISCHE STARTUP-MELDUNGEN:")
    print("-" * 30)
    print("✅ Positive Zeichen in Logs:")
    print("   - 'Starting nginx'")
    print("   - 'Starting supervisor'") 
    print("   - 'docassemble: Starting'")
    print("   - 'docassemble: Ready'")
    print("   - 'PostgreSQL database system is ready'")
    print("   - 'Apache/Nginx started'")
    print("")
    print("🚨 Problem-Indikatoren:")
    print("   - 'ERROR' oder 'FATAL'")
    print("   - 'Connection refused'")
    print("   - 'Database connection failed'")
    print("   - 'Memory allocation failed'")
    print("   - 'Disk space'")
    print("")
    
    print("⏱️ STARTUP-ZEITEN:")
    print("-" * 20)
    print("   - Container Start: 10-30 Sekunden")
    print("   - Database Init: 30-60 Sekunden")
    print("   - Docassemble Init: 60-120 Sekunden")
    print("   - Web-Services: 30-60 Sekunden")
    print("   - Gesamt: 2-5 Minuten (normal)")
    print("   - Bei Problemen: 5-15 Minuten")
    print("")
    
    print("🔧 PRAKTISCHE LOG-BEFEHLE:")
    print("-" * 25)
    
    # Windows PowerShell Commands
    print("# FÜR POWERSHELL (Windows):")
    print('docker ps | Select-String "docassemble"')
    print('docker logs -f $(docker ps -q --filter "ancestor=jhpyle/docassemble")')
    print("")
    
    # Alternative wenn Container-Name bekannt
    print("# FALLS CONTAINER-NAME BEKANNT (z.B. 'docassemble'):")
    print("docker logs -f docassemble")
    print("")
    
    print("🎯 SOFORTIGER BEFEHL FÜR SIE:")
    print("-" * 30)
    print("Führen Sie JETZT in einem neuen Terminal aus:")
    print("")
    print("docker logs -f $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("")
    print("Das zeigt Ihnen Live-Logs während des Startvorgangs!")
    print("")
    
    print("📱 MONITORING-KOMBINATION:")
    print("-" * 25)
    print("Terminal 1 (Live Logs):")
    print("  docker logs -f $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("")
    print("Terminal 2 (Service Test):")
    print("  # Unser Python Monitor läuft bereits")
    print("  # Oder manuell: curl -I http://192.168.178.29:8080/")
    print("")
    
    print("🔍 TROUBLESHOOTING:")
    print("-" * 20)
    print("Falls Container nicht gefunden:")
    print("  docker ps -a  # Alle Container anzeigen")
    print("  docker images | grep docassemble  # Images prüfen")
    print("")
    print("Falls Logs zu schnell:")
    print("  docker logs --tail 20 <CONTAINER>  # Nur letzte 20 Zeilen")
    print("  docker logs <CONTAINER> | less  # Mit Pager")

if __name__ == "__main__":
    show_container_logs()

"""
Docassemble Container Port und Login Problem
Nach Neustart: Port 80 statt 8080, Login funktioniert nicht mehr
"""

def analyze_port_login_problem():
    print("🚨 CONTAINER NEUSTART PROBLEM ANALYSE")
    print("="*45)
    
    print("📋 IDENTIFIZIERTE PROBLEME:")
    print("-" * 30)
    print("   🔌 Port-Problem: Container läuft auf Port 80 statt 8080")
    print("   🔐 Login-Problem: Admin-Credentials funktionieren nicht")
    print("   🗄️ Wahrscheinlich: Neue/Leere Datenbank")
    print("   💾 Volume-Mount evtl. nicht korrekt")
    
    print("\n🔍 SOFORTIGE DIAGNOSE:")
    print("-" * 25)
    print("   # Aktuelle Container prüfen:")
    print("   docker ps")
    print("   ")
    print("   # Port-Mapping prüfen:")
    print("   docker port $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("   ")
    print("   # Volume-Mounts prüfen:")
    print("   docker inspect $(docker ps -q --filter ancestor=jhpyle/docassemble) | grep -A 10 Mounts")
    
    print("\n🛠️ LÖSUNGSANSÄTZE:")
    print("-" * 20)
    
    print("   OPTION 1: KORREKTEN PORT ZUGREIFEN")
    print("   # Falls Container auf Port 80 läuft:")
    print("   curl -I http://192.168.178.29:80/")
    print("   # Im Browser: http://192.168.178.29/")
    print("   ")
    print("   # Falls Container auf anderem Port:")
    print("   curl -I http://192.168.178.29:8080/")
    print("   # Im Browser: http://192.168.178.29:8080/")
    
    print("\n   OPTION 2: CONTAINER MIT KORREKTEM PORT NEUSTARTEN")
    print("   # Aktuellen Container stoppen:")
    print("   docker stop $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("   ")
    print("   # Mit korrektem Port-Mapping starten:")
    print("   docker run -d --name docassemble_correct \\")
    print("     -p 8080:80 \\")
    print("     -v /var/docassemble:/usr/share/docassemble \\")
    print("     --memory=4g \\")
    print("     --restart=unless-stopped \\")
    print("     jhpyle/docassemble:latest")
    
    print("\n🔐 LOGIN-PROBLEME LÖSEN:")
    print("-" * 25)
    
    print("   SZENARIO 1: NEUE INSTALLATION")
    print("   Falls Volume leer war:")
    print("   - Standard-Admin wird erstellt")
    print("   - Credentials: admin@admin.com / password")
    print("   - Oder: admin@example.com / admin")
    print("   - Oder: Initial Setup erforderlich")
    
    print("\n   SZENARIO 2: DATENBANK ZURÜCKGESETZT")
    print("   # Container-Logs prüfen auf Initial Setup:")
    print("   docker logs $(docker ps -q --filter ancestor=jhpyle/docassemble) | grep -i admin")
    print("   docker logs $(docker ps -q --filter ancestor=jhpyle/docassemble) | grep -i password")
    print("   docker logs $(docker ps -q --filter ancestor=jhpyle/docassemble) | grep -i initial")
    
    print("\n   SZENARIO 3: INITIAL SETUP ERFORDERLICH")
    print("   # Bei neuer Installation:")
    print("   1. Gehen Sie zu: http://192.168.178.29:<PORT>/")
    print("   2. Folgen Sie dem Initial Setup Wizard")
    print("   3. Erstellen Sie neuen Admin-User")
    
    print("\n⚡ SCHNELLE TESTS:")
    print("-" * 18)
    
    test_urls = [
        "http://192.168.178.29/",
        "http://192.168.178.29:80/", 
        "http://192.168.178.29:8080/",
        "http://192.168.178.29/user/sign-in",
        "http://192.168.178.29:8080/user/sign-in"
    ]
    
    for url in test_urls:
        print(f"   curl -I {url}")
    
    print("\n🔧 ADMIN RESET (FALLS NÖTIG):")
    print("-" * 30)
    print("   # Im Container Admin-User erstellen:")
    print("   docker exec -it $(docker ps -q --filter ancestor=jhpyle/docassemble) bash")
    print("   ")
    print("   # Dann im Container:")
    print("   da create_admin_user admin@admin.com password")
    print("   # Oder:")
    print("   python -m docassemble.webapp.create_admin admin@admin.com password")
    
    print("\n📊 VOLUME DATEN PRÜFEN:")
    print("-" * 25)
    print("   # Host-Verzeichnis prüfen:")
    print("   ls -la /var/docassemble/")
    print("   ls -la /var/docassemble/config/")
    print("   ")
    print("   # Database-File prüfen:")
    print("   ls -la /var/docassemble/db/")
    print("   ")
    print("   # Falls Backup vorhanden:")
    print("   ls -la /var/docassemble/backup/")
    
    print("\n🎯 EMPFOHLENES VORGEHEN:")
    print("-" * 25)
    print("   1. 🔍 Container-Status prüfen (docker ps)")
    print("   2. 🌐 Korrekte URL im Browser testen")
    print("   3. 🔐 Standard-Logins versuchen")
    print("   4. 📊 Logs auf Initial Setup prüfen")
    print("   5. 🛠️ Falls nötig: Admin-User manuell erstellen")
    print("   6. 💾 Volume-Daten auf Vollständigkeit prüfen")
    
    print("\n⚠️ BACKUP-STRATEGIE:")
    print("-" * 20)
    print("   # Aktuelle Daten sichern:")
    print("   docker exec $(docker ps -q --filter ancestor=jhpyle/docassemble) da backup")
    print("   ")
    print("   # Backup-Dateien:")
    print("   ls -la /var/docassemble/backup/")
    
    print("\n📝 LOGIN-KOMBINATIONEN ZUM TESTEN:")
    print("-" * 35)
    login_combos = [
        "admin@admin.com / password",
        "admin@example.com / admin", 
        "admin@admin.com / admin",
        "admin@example.com / password",
        "admin / admin",
        "administrator / password"
    ]
    
    for combo in login_combos:
        print(f"   🔐 {combo}")
    
    print("\n🚀 SCHNELLE LÖSUNG:")
    print("-" * 20)
    print("   # Container-Port ermitteln:")
    print("   docker port $(docker ps -q --filter ancestor=jhpyle/docassemble)")
    print("   ")
    print("   # Dann im Browser die korrekte URL:")
    print("   http://192.168.178.29:<GEFUNDENER_PORT>/")

if __name__ == "__main__":
    analyze_port_login_problem()

"""
Docker Container Restart Commands
Für die Behebung des Nginx-Backend Problems
"""

print("🐳 DOCKER CONTAINER RESTART LÖSUNG")
print("="*40)

print("💡 PROBLEM ZUSAMMENFASSUNG:")
print("   - Nur Root-Page (/) funktioniert")
print("   - Alle anderen Admin-Routes → 502 Bad Gateway") 
print("   - APIs funktionieren noch")
print("   - Nginx kann Backend nicht erreichen")

print("\n🛠️ BEFEHLE FÜR CONTAINER RESTART:")
print("-" * 35)

print("# 1. Container Status prüfen")
print("docker ps")
print("docker ps | grep docassemble")
print("")

print("# 2. Container Logs anschauen (letzten 50 Zeilen)")  
print("docker logs <CONTAINER_NAME> --tail 50")
print("# Oder wenn Sie den Namen nicht wissen:")
print("docker logs $(docker ps | grep docassemble | awk '{print $1}') --tail 50")
print("")

print("# 3. Container Restart")
print("docker restart <CONTAINER_NAME>")
print("# Oder automatisch:")
print("docker restart $(docker ps | grep docassemble | awk '{print $1}')")
print("")

print("# 4. Warten auf Neustart (2-3 Minuten)")
print("echo 'Warte auf Container-Start...'")
print("sleep 180")
print("")

print("# 5. Status überprüfen")
print("curl -I http://192.168.178.29:8080/")
print("curl -I http://192.168.178.29:8080/updatepackage")

print("\n⚡ SCHNELLE ALL-IN-ONE LÖSUNG:")
print("-" * 30)
print("docker restart $(docker ps | grep docassemble | awk '{print $1}') && echo 'Container wird neu gestartet...' && sleep 180 && curl -I http://192.168.178.29:8080/updatepackage")

print("\n🔍 ALTERNATIVE: NEUER CONTAINER")
print("-" * 30)
print("# Falls Restart nicht hilft:")
print("docker stop <CONTAINER_NAME>")
print("docker run -d --name docassemble_new \\")
print("  -p 8080:80 \\") 
print("  -v /var/docassemble:/usr/share/docassemble \\")
print("  jhpyle/docassemble:latest")

print("\n📞 NACH DEM RESTART TESTEN:")
print("-" * 30)
print("1. Browser: http://192.168.178.29:8080/")
print("2. Package Update: http://192.168.178.29:8080/updatepackage")
print("3. Admin Interface: Navigation über Weboberfläche")

print("\n⏱️ GESCHÄTZTER ZEITAUFWAND:")
print("   - Container Restart: 3-5 Minuten")
print("   - Service vollständig verfügbar: 5-10 Minuten")
print("   - Problem sollte dann behoben sein")

print("\n🚨 WICHTIG:")
print("   - Das ist ein Container/Nginx Problem, nicht unser MCP Server")
print("   - APIs funktionieren weiterhin")
print("   - Nach Restart sollte alles wieder normal laufen")

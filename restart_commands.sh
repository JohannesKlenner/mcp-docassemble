#!/bin/bash
# Docassemble Container Neustart mit korrekten Credentials
# Basierend auf docassemble.env: admin@example.com / admin

echo "🔄 Docassemble Container Neustart mit korrekten Credentials"
echo "============================================================"

# 1. Aktuellen Container finden und stoppen
echo "📊 1. Aktuelle Container anzeigen:"
docker ps

echo ""
echo "⏹️  2. Container stoppen (ersetzen Sie CONTAINER_ID mit der echten ID):"
echo "docker stop -t 600 CONTAINER_ID"
echo ""
echo "🗑️  3. Container entfernen:"
echo "docker rm CONTAINER_ID"
echo ""

# 2. Neuen Container mit korrekten Credentials starten
echo "🚀 4. Neuen Container mit korrekten Admin-Credentials starten:"
echo ""
echo "docker run -d -p 80:80 \\"
echo "  -e DA_ADMIN_EMAIL=admin@example.com \\"
echo "  -e DA_ADMIN_PASSWORD=admin \\"
echo "  -e DA_DEFAULT_LOCALIZATION=de-DE \\"
echo "  --restart always \\"
echo "  --stop-timeout 600 \\"
echo "  jhpyle/docassemble"
echo ""

# 3. Status prüfen
echo "📋 5. Nach dem Start prüfen:"
echo "docker ps"
echo "docker logs [NEW_CONTAINER_ID]"
echo ""

# 4. Login testen
echo "🧪 6. Login testen nach ca. 2-3 Minuten:"
echo "URL: http://192.168.178.29:80"
echo "Email: admin@example.com"
echo "Password: admin"
echo ""

echo "⚠️  WICHTIG:"
echo "- Container braucht 2-3 Minuten zum vollständigen Start"
echo "- Warten Sie auf 'nginx started' in den Logs"
echo "- Dann erst Login versuchen"

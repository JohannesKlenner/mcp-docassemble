#!/bin/bash
# Befehle für den Server (johannes@192.168.178.29)

echo "=== 1. Aktuellen Container prüfen ==="
docker ps

echo -e "\n=== 2. Container stoppen ==="
# Ersetzen Sie CONTAINER_ID mit der tatsächlichen ID aus Schritt 1
docker stop -t 600 CONTAINER_ID

echo -e "\n=== 3. Container entfernen ==="
docker rm CONTAINER_ID

echo -e "\n=== 4. Prüfen ob .env Datei existiert ==="
ls -la ~/docassemble.env
cat ~/docassemble.env

echo -e "\n=== 5. Container mit .env Datei starten ==="
docker run -d \
  --name docassemble \
  -p 80:80 \
  --env-file ~/docassemble.env \
  jhpyle/docassemble

echo -e "\n=== 6. Container Logs überwachen ==="
echo "Warten auf Container Start..."
docker logs -f docassemble

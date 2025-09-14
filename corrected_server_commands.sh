#!/bin/bash
# Korrigierte Befehle für den Server

echo "=== 1. Aktuellen Container stoppen (falls vorhanden) ==="
docker ps
# Falls ein Container läuft, stoppen Sie ihn mit:
# docker stop CONTAINER_ID
# docker rm CONTAINER_ID

echo -e "\n=== 2. Prüfen der .env Datei ==="
ls -la ./docassemble.env
cat ./docassemble.env

echo -e "\n=== 3. Container mit korrektem Befehl starten ==="
docker run -d \
  -p 80:80 \
  -p 443:443 \
  --env-file ./docassemble.env \
  --restart always \
  --stop-timeout 600 \
  --name docassemble \
  jhpyle/docassemble

echo -e "\n=== 4. Container Status prüfen ==="
docker ps

echo -e "\n=== 5. Container Logs überwachen ==="
docker logs -f docassemble

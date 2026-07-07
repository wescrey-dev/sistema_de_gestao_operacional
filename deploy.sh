#!/bin/bash
set -e
cd /var/www/web_app
echo "Puxando alterações do GitHub..."
git pull origin main
echo "Reiniciando o serviço..."
sudo systemctl restart webapp
echo "Deploy concluído!"

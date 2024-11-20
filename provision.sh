#!/bin/bash

# Establecer el modo no interactivo para evitar prompts durante las instalaciones
export DEBIAN_FRONTEND=noninteractive

# Actualizar el sistema
sudo apt-get update -y
sudo apt-get upgrade -y

# Instalar dependencias necesarias: Python, MariaDB y herramientas adicionales
sudo apt-get install -y python3-pip python3-dev mariadb-server libmariadb-dev screen

# Iniciar y asegurar la instalación de MariaDB
sudo systemctl start mariadb
sudo systemctl enable mariadb > /dev/null 2>&1
sudo systemctl restart mariadb > /dev/null 2>&1


# Cargar las variables del archivo .env
set -a
source /home/vagrant/app/.env
set +a

# Crear base de datos y usuario solo si no existen
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $DATABASE_DB;"
sudo mysql -e "CREATE USER IF NOT EXISTS '$DATABASE_USER'@'localhost' IDENTIFIED BY '$DATABASE_PASSWORD';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $DATABASE_DB.* TO '$DATABASE_USER'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Cambiar al directorio de la aplicación
cd /home/vagrant/app

# Instalar las dependencias de la aplicación
pip3 install --upgrade pip
pip3 install --ignore-installed -r requirements.txt

# Configurar permisos para que el usuario vagrant tenga acceso completo
sudo chown -R vagrant:vagrant /home/vagrant/app

# Lanzar la aplicación Flask en segundo plano con screen
screen -m -d -S flask_app bash -c "source /home/vagrant/app/.env && python3 /home/vagrant/app/app.py"

# Mensaje de finalización
echo "¡Aprovisionamiento completado y aplicación lanzada en http://localhost:8080!"
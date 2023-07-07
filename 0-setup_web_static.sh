#!/usr/bin/env bash
# This script sets up your webservers for deployment
# of web_static

# update and install nginx if not installed
sudo apt-get update
sudo apt-get install nginx

if [ ! -d "/data/" ]
then
        sudo mkdir /data/
fi

if [ ! -d "/data/web_static/" ]
then
        sudo mkdir /data/web_static/
fi

if [ ! -d "/data/web_static/releases/" ]
then
        sudo mkdir /data/web_static/releases/
fi

if [ ! -d "/data/web_static/shared/" ]
then
        sudo mkdir /data/web_static/shared/
fi

if [ ! -d "/data/web_static/releases/test/" ]
then
        sudo mkdir /data/web_static/releases/test/
fi

echo "<h1>Hello World</h1>" | sudo tee /data/web_static/releases/test/index.html

# If symbolic link exists, delete it and create another
if [ -L "/data/web_static/current" ]
then
        sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

# Update the nginx config to be able to serve content
config="server_name _;\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "s|server_name _;|$config|1" /etc/nginx/sites-available/default

sudo service nginx restart

exit 0

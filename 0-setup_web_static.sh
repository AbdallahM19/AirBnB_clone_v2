#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deployment of web_static. It must:

sudo apt-get -y update
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get install -y nginx
fi
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

sudo echo 'this is fake HTML file' > /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"
static_alias="location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }\
"

sudo sed -i '/listen 80 default_server/a '"$static_alias" "$config_file"

if pgrep "nginx" > /dev/null; then
    sudo service nginx restart
else
    sudo service nginx start
fi


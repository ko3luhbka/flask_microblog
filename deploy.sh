#!/usr/bin/env bash

sudo apt -y update

# Install and configure firewall
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 443/tcp
sudo ufw --force enable

# Install other dependencies
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt -y install python3.7 python3-dev python3.7-venv
sudo apt -y install supervisor nginx git
# `mysql-server` should be installed manually 

# Clone the repo
git clone https://github.com/ko3luhbka/flask_microblog.git
cd flask_microblog

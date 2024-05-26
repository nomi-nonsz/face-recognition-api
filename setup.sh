#!/bin/bash
# Run as root

apt --version
apt update -y && apt upgrade -y
apt install -y curl tmux

# Installing Node
# https://github.com/nodesource/distributions
curl -fsSL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt install -y nodejs
node -v
npm -v
npm i -g yarn

# Installing Python
apt install python3 python3-full cmake pip -y
python3 -m venv .venv
source /.venv/bin/activate
python3 -m pip install -r requirements.txt

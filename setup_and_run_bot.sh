#!/bin/bash

# Update package list and install dependencies
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip

# Navigate to the directory where the bot script is located
cd /home/ec2-user/discord-bot/src

# Install required Python packages
pip3 install -r requirements.txt

# Run the Discord bot
nohup python3 main.py &

echo "Discord bot is now running."

#!/bin/bash

# Update package list and install dependencies
sudo yum update -y

# Install Python and pip
sudo yum install -y python3 python3-pip

# Navigate to the directory where the bot script is located
cd /home/ec2-user/discord-bot/src

# Install required Python packages
pip3 install -r requirement.txt

# Run the Discord bot
nohup python3 main.py &

echo "Discord bot is now running."

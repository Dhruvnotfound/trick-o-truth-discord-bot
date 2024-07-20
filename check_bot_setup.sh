#!/bin/bash
   

   # SSH into the ec2 instance to run this
   # ssh -i /path/to/your/key.pem ec2-user@<public_ip_address>
   echo "Checking Discord bot setup..."

   # Check if the discord-bot directory exists
   if [ -d "/home/ec2-user/discord-bot" ]; then
       echo "✅ discord-bot directory exists"
   else
       echo "❌ discord-bot directory not found"
   fi

   # Check if the .env file exists and contains the TOKEN
   if [ -f "/home/ec2-user/discord-bot/.env" ] && grep -q "TOKEN=" "/home/ec2-user/discord-bot/.env"; then
       echo "✅ .env file exists and contains TOKEN"
   else
       echo "❌ .env file is missing or doesn't contain TOKEN"
   fi

   # Check if the setup_and_run_bot.sh script exists and is executable
   if [ -x "/home/ec2-user/discord-bot/setup_and_run_bot.sh" ]; then
       echo "✅ setup_and_run_bot.sh exists and is executable"
   else
       echo "❌ setup_and_run_bot.sh is missing or not executable"
   fi

   # Check if Python and pip are installed
   if command -v python3 &>/dev/null && command -v pip3 &>/dev/null; then
       echo "✅ Python and pip are installed"
   else
       echo "❌ Python and/or pip are not installed"
   fi

   # Check if required Python packages are installed
   if pip3 list | grep -q "discord" && pip3 list | grep -q "asyncio"; then
       echo "✅ Required Python packages are installed"
   else
       echo "❌ Some required Python packages are missing"
   fi

   # Check if the bot process is running
   if pgrep -f "python3 main.py" > /dev/null; then
       echo "✅ Discord bot process is running"
   else
       echo "❌ Discord bot process is not running"
   fi

   echo "Check complete."
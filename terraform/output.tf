# Output the public IP of the EC2 instance
output "discord_bot_public_ip" {
  value = aws_instance.discord_bot_instance.public_ip
}
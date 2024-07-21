# Create a VPC
resource "aws_vpc" "discord_bot_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "Discord Bot VPC"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "discord_bot_igw" {
  vpc_id = aws_vpc.discord_bot_vpc.id

  tags = {
    Name = "Discord Bot IGW"
  }
}

# Create a Subnet
resource "aws_subnet" "discord_bot_subnet" {
  vpc_id     = aws_vpc.discord_bot_vpc.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "Discord Bot Subnet"
  }
}

# Create a Route Table
resource "aws_route_table" "discord_bot_route_table" {
  vpc_id = aws_vpc.discord_bot_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.discord_bot_igw.id
  }

  tags = {
    Name = "Discord Bot Route Table"
  }
}

# Associate the Route Table with the Subnet
resource "aws_route_table_association" "discord_bot_route_assoc" {
  subnet_id      = aws_subnet.discord_bot_subnet.id
  route_table_id = aws_route_table.discord_bot_route_table.id
}

# Create a Security Group
resource "aws_security_group" "discord_bot_sg" {
  name        = "discord_bot_sg"
  description = "Security group for Discord bot EC2 instance"
  vpc_id      = aws_vpc.discord_bot_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Discord Bot Security Group"
  }
}

# Create an EC2 Instance
resource "aws_instance" "discord_bot_instance" {
  ami           = "ami-0b72821e2f351e396"
  instance_type = "t2.micro"
  key_name      = "discord_bot" # Replace with your key pair name

  vpc_security_group_ids = [aws_security_group.discord_bot_sg.id]
  subnet_id              = aws_subnet.discord_bot_subnet.id

  associate_public_ip_address = true

  tags = {
    Name = "Discord Bot EC2 Instance"
  }
  #use aws secret manager?
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y git python3-pip
              cd /home/ec2-user
              git clone https://github.com/Dhruvnotfound/trick-o-truth-discord-bot.git discord-bot
              cd discord-bot
              echo "TOKEN=${local.token["Discord_bot_token"]}" > .env
              chmod +x setup_and_run_bot.sh
              ./setup_and_run_bot.sh 
              EOF
}
resource "aws_s3_bucket" "bot_files_bucket" {
  bucket = "my-discord-bot-files-bucket" # Change this to a unique name
  acl    = "private"

  tags = {
    Name = "Discord Bot Files Bucket"
  }
}

# Upload your bot files to S3
resource "aws_s3_bucket_object" "bot_file" {
  bucket = aws_s3_bucket.bot_files_bucket.id
  key    = "bot.py"  # The name of the file in S3
  source = "../path/to/your/bot.py"  # Path to your local bot file
}

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
    cidr_blocks = ["0.0.0.0/0"]  # Be cautious with this. In production, limit to your IP.
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
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI (HVM), SSD Volume Type
  instance_type = "t2.micro"
  key_name      = "your-key-pair-name"  # Replace with your key pair name

  vpc_security_group_ids = [aws_security_group.discord_bot_sg.id]
  subnet_id              = aws_subnet.discord_bot_subnet.id

  associate_public_ip_address = true

  tags = {
    Name = "Discord Bot EC2 Instance"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 pip
              pip3 install discord.py
              aws s3 cp s3://${aws_s3_bucket.bot_files_bucket.id}/bot.py /home/ec2-user/bot.py
              # Add any other necessary setup commands here
              EOF
# Add IAM role to allow S3 access
  iam_instance_profile = aws_iam_instance_profile.ec2_s3_profile.name
}

# Create IAM role and instance profile
resource "aws_iam_role" "ec2_s3_access_role" {
  name = "ec2_s3_access_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_access_policy" {
  role       = aws_iam_role.ec2_s3_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_instance_profile" "ec2_s3_profile" {
  name = "ec2_s3_profile"
  role = aws_iam_role.ec2_s3_access_role.name
}

# Output the public IP of the EC2 instance
output "discord_bot_public_ip" {
  value = aws_instance.discord_bot_instance.public_ip
}
variable "ami" {
  description = "AMI ID for the EC2 instance"
  default     = "ami-0b72821e2f351e396"
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  default     = "t2.micro"
}

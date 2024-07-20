data "aws_secretsmanager_secret_version" "bot_token" {
  secret_id = "arn:aws:secretsmanager:us-east-1:435202373383:secret:trick-o-truth-bot-token-WkNcZL"
}
locals {
  token = jsondecode(data.aws_secretsmanager_secret_version.bot_token.secret_string)
}
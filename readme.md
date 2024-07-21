# Trick-o-Truth Discord bot 

A Discord bot built with Python and discord.py to play a fun party game called "Trick or Truth".


## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Deployment (using AWS EC2)](#Deployment-(using-AWS-EC2)) (paid)
5. [Deployment (using Replit)](#Deployment-(using-Replit)) (free with limits)
6. [About game](#About-Game)
7. [Contributing](#contributing)
8. [License](#license) 
9. [Contact](#contact)

## Project Description

Trick-o-Truth is an engaging Discord bot designed to spice up your server with a fun and interactive game. Players take turns being the "truth-teller", providing truths about themselves while others try to deceive or guess correctly. It's a great way to break the ice, get to know your friends better, and have a good laugh!
For detailed game rules click [About game](#About-Game)  
add this bot to your server using the link- [https://discord.com/oauth2/authorize?client_id=1262113443025125516&permissions=277025877072&integration_type=0&scope=bot] (offline)

## Features

- Interactive gameplay with multiple rounds
- Scoring system to track player performance
- Automatic game flow management
- User-friendly commands for easy interaction

## Prerequisites

Before you begin, ensure you have met the following requirements:
- A Discord account and a registered Discord application/bot
- An AWS account (for deployment)
- Terraform (for IaC automotaion)
- python3 (for discord bot) 

## Deployment (using AWS EC2)

To install Trick-o-Truth Bot, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/Dhruvnotfound/trick-o-truth-discord-bot.git
   cd trick-o-truth-discord-bot
   ```

2. Change the provider credentials to your AWS account credentials

3. Change the aws secret arn with your own secret arn containing your discord bot token and the key-pair name of your ec2 instance. You can remove the hardcode the values in the code as well but not adviced due to security measures.

4. After making all the changes as per your requirements run 
    ```
    terraform init
    ```
    ```
    terraform apply -auto-approve
    ```
```
This will Run the discord bot online!!
```

## Deployment (using Replit)
1. create a free account on Replit
2. visit [template](https://replit.com/@dhruvgupta3107/trick-o-truth?v=1) and click use template
3. set up your discord bot token as a secret with the name "TOKEN"
4. click RUN
```
This will make your bot online until the browser tab is open and the limit is not reached for free.
```

## About Game
### Game Overview 🎮

Players take turns being the 'truth teller'. Each round, one player provides a truth about themselves, while others provide fake truths. Everyone then guesses which statement is the real truth.

### How to Play 🕹️
Use !start to begin a new game.  
Players join by clicking the 'Join Game' button.  
Each round, one player is chosen as the truth-teller.  
The truth-teller provides a truth about themselves via DM.  
Other players provide fake truths about the truth-teller via DM.  
All truths are displayed, and players guess the real one by clicking the corresponding button.  
Points are awarded based on correct guesses and successful deception.  
The game continues until all players have been the truth-teller.
Scoring System 🏆  
• Correct guess: +10 points  
• Successfully deceiving others: +5 points per player fooled  

### Commands 🛠️  
`!start` - Start a new game  
`!stop` - Stop the current game  
`!help` - Show this help message  
Tips 💡  
• Be creative with your truths and fake truths!  
• Pay attention to other players' writing styles.  
• Don't be too obvious with your fake truths.  
• Have fun and get to know your friends better!  
• Minimum number of players is 2, but 4+ players is recommended for more fun!

## Contributing

To contribute to Trick-o-Truth Bot, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`.
4. Push to the original branch: `git push origin <project_name>/<location>`.
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project uses the following license: [MIT License](https://opensource.org/licenses/MIT).

## Contact

If you want to contact the maintainer, you can reach out at [dhruvgupta3107@gmail.com].

---

Thank you for your interest in the Trick-o-Truth Discord Bot! We hope you enjoy using it as much as we enjoyed creating it. If you have any questions, issues, or suggestions, please don't hesitate to open an issue or submit a pull request. Happy gaming! 🎉
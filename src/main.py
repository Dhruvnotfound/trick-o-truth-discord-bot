import discord
from discord.ext import commands
import random
import asyncio
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

class TruthGame:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.truths = {}
        self.scores = {}
        self.game_in_progress = False

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
            self.scores[player] = 0
            return True
        return False

    def start_game(self):
        if len(self.players) < 2:
            return False
        random.shuffle(self.players)
        self.game_in_progress = True
        return True

    def stop_game(self):
        self.game_in_progress = False

    def next_player(self):
        if not self.players:
            return None
        if self.current_player is None:
            self.current_player = self.players[0]
        else:
            current_index = self.players.index(self.current_player)
            if current_index == len(self.players) - 1:
                return None
            self.current_player = self.players[current_index + 1]
        return self.current_player

    def add_truth(self, player, truth):
        if player not in self.truths:
            self.truths[player] = []
        self.truths[player].append(truth)

    def get_truths(self, player):
        return self.truths.get(player, [])

    def update_score(self, guesser, truth_teller, fake_truth_author, correct):
        if correct:
            self.scores[guesser] += 10
        else:
            self.scores[fake_truth_author] += 5

    def get_scores(self):
        return self.scores

    def get_winners(self):
        max_score = max(self.scores.values())
        return [player for player, score in self.scores.items() if score == max_score]

    def reset(self):
        self.__init__()

game = TruthGame()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord! 🎉')
    await bot.change_presence(activity=discord.Game(name="Trick-o-Truth | Type !help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("I don't have the necessary permissions to execute this command. 😢")
    elif isinstance(error, discord.Forbidden):
        await ctx.send("I'm lacking permissions to perform this action. 😢")
    else:
        raise error

@bot.command(name='start')
async def start_game(ctx):
    global game
    if game.game_in_progress:
        await ctx.send("A game is already in progress! 🚫")
        return

    view = discord.ui.View()
    button = discord.ui.Button(label="Join Game", style=discord.ButtonStyle.green)

    async def join_callback(interaction):
        if game.add_player(interaction.user):
            await interaction.response.send_message(f"{interaction.user.name} has joined the game! ✅")
        else:
            await interaction.response.send_message(f"{interaction.user.name} is already in the game! 🚫", ephemeral=True)

    button.callback = join_callback
    view.add_item(button)

    await ctx.send("A new game is starting! Click the button to join! 🕹️", view=view)

    # Add timer countdown before start
    for i in range(30, 0, -10):
        await ctx.send(f"Game starting in {i} seconds...")
        await asyncio.sleep(10)

    if game.start_game():
        await ctx.send(f"Game started with {len(game.players)} players! 🎮 \n check your dms 💌")
        await play_round(ctx)
    else:
        await ctx.send("Not enough players to start the game. Minimum 2 players required. 🚫")
        game.reset()

@bot.command(name='stop')
async def stop_game(ctx):
    global game
    if not game.game_in_progress:
        await ctx.send("There is no game in progress to stop. 🚫")
        return

    game.stop_game()
    await ctx.send("The game has been stopped. 🛑")
    await end_game(ctx)

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="Help 📚",
        description="Welcome to the Trick-o-truth! Test your knowledge of your friends and your ability to deceive.",
        color=0x00ff00
    )

    embed.add_field(
        name="Game Overview 🎮",
        value="Players take turns being the 'truth teller'. Each round, one player provides a truth about themselves, while others provide fake truths. Everyone then guesses which statement is the real truth.",
        inline=False
    )

    embed.add_field(
        name="How to Play 🕹️",
        value=(
            "1. Use `!start` to begin a new game.\n"
            "2. Players join by clicking the 'Join Game' button.\n"
            "3. Each round, one player is chosen as the truth-teller.\n"
            "4. The truth-teller provides a truth about themselves via DM.\n"
            "5. Other players provide fake truths about the truth-teller via DM.\n"
            "6. All truths are displayed, and players guess the real one by clicking the corresponding button.\n"
            "7. Points are awarded based on correct guesses and successful deception.\n"
            "8. The game continues until all players have been the truth-teller."
        ),
        inline=False
    )

    embed.add_field(
        name="Scoring System 🏆",
        value=(
            "• Correct guess: +10 points\n"
            "• Successfully deceiving others: +5 points per player fooled"
        ),
        inline=False
    )

    embed.add_field(
        name="Commands 🛠️",
        value=(
            "`!start` - Start a new game\n"
            "`!stop` - Stop the current game\n"
            "`!help` - Show this help message"
        ),
        inline=False
    )

    embed.add_field(
        name="Tips 💡",
        value=(
            "• Be creative with your truths and fake truths!\n"
            "• Pay attention to other players' writing styles.\n"
            "• Don't be too obvious with your fake truths.\n"
            "• Have fun and get to know your friends better!\n"
            "• Minimum number of players is 2, but 4+ players is recommended for more fun!"
        ),
        inline=False
    )

    embed.set_footer(text="Remember to keep it friendly and respectful. Enjoy the game!")

    await ctx.send(embed=embed)

async def play_round(ctx):
    global game
    if not game.game_in_progress:
        return

    current_player = game.next_player()

    if current_player is None:
        await end_game(ctx)
        return

    # Send prompts to all players simultaneously
    truth_tasks = []
    fake_truth_tasks = []
    for player in game.players:
        if player == current_player:
            truth_tasks.append(player.send("Please enter one truth about yourself. 🤔"))
        else:
            fake_truth_tasks.append(player.send(f"Please enter a fake truth about {current_player.name}. 🤥"))

    # Wait for all messages to be sent
    await asyncio.gather(*truth_tasks, *fake_truth_tasks)

    # Set up checks for truth and fake truths
    def truth_check(m):
        return m.author == current_player and isinstance(m.channel, discord.DMChannel)

    def fake_truth_check(m):
        return m.author != current_player and m.author in game.players and isinstance(m.channel, discord.DMChannel)

    # Wait for responses with a timeout
    truth_response = None
    fake_truths = []
    timeout = 90.0

    async def collect_responses():
        nonlocal truth_response
        try:
            truth_response = await asyncio.wait_for(bot.wait_for('message', check=truth_check), timeout=timeout)
        except asyncio.TimeoutError:
            pass

        while len(fake_truths) < len(game.players) - 1:
            try:
                fake_truth = await asyncio.wait_for(bot.wait_for('message', check=fake_truth_check), timeout=timeout)
                fake_truths.append((fake_truth.author, fake_truth.content))
            except asyncio.TimeoutError:
                break

    try:
        await asyncio.wait_for(collect_responses(), timeout=timeout)
    except asyncio.TimeoutError:
        pass

    # Handle responses
    if truth_response is None:
        await ctx.send(f"{current_player.name} didn't provide a truth. Moving to the next player. ⏳")
        await play_round(ctx)
        return

    all_truths = [truth_response.content] + [truth for _, truth in fake_truths]
    random.shuffle(all_truths)

    # Continue with the guessing phase
    truth_options = "\n".join([f"{i+1}. {truth}" for i, truth in enumerate(all_truths)])
    embed = discord.Embed(title=f"Time to guess! 🔍", description=f"Which one is the truth about {current_player.name}?\n{truth_options}", color=0x00ff00)

    # Create buttons for guessing
    class GuessView(discord.ui.View):
        def __init__(self, num_options, timeout=30):
            super().__init__(timeout=timeout)
            self.guesses = {}
            self.num_options = num_options
            self.create_buttons()

        def create_buttons(self):
            for i in range(1, self.num_options + 1):
                button = discord.ui.Button(label=str(i), style=discord.ButtonStyle.primary, custom_id=str(i))
                button.callback = self.button_callback
                self.add_item(button)

        async def button_callback(self, interaction: discord.Interaction):
            guess = int(interaction.data['custom_id'])
            if interaction.user == current_player or interaction.user in self.guesses:
                await interaction.response.send_message("You can't guess!", ephemeral=True)
                return
            self.guesses[interaction.user] = guess
            await interaction.response.send_message(f"You guessed option {guess}", ephemeral=True)

    view = GuessView(len(all_truths))
    guess_message = await ctx.send(embed=embed, view=view)

    # Wait for 20 seconds
    await asyncio.sleep(20)

    # Send a 10-second warning
    await ctx.send("10 seconds remaining for guessing!")

    # Wait for the final 10 seconds
    await asyncio.sleep(10)

    # Disable buttons after time is up
    view.stop()
    for child in view.children:
        child.disabled = True
    await guess_message.edit(view=view)

    correct_index = all_truths.index(truth_response.content)

    # Process guesses and update scores
    for guesser, guess in view.guesses.items():
        if guess == correct_index + 1:
            game.update_score(guesser, current_player, None, True)
            await ctx.send(f"{guesser.name} guessed correctly! 🎉 +10 points")
        else:
            fake_truth_author = next((author for author, content in fake_truths if content == all_truths[guess-1]), None)
            if fake_truth_author:
                game.update_score(guesser, current_player, fake_truth_author, False)
                await ctx.send(f"{guesser.name} guessed incorrectly. ❌ +5 points to {fake_truth_author.name}")
            else:
                await ctx.send(f"{guesser.name} guessed incorrectly.")

    await ctx.send(f"The correct truth was: {truth_response.content}")
    embed = discord.Embed(title="Current scores 📊", color=0x00ff00)
    for player, score in game.get_scores().items():
        embed.add_field(name=player.name, value=score, inline=False)
    await ctx.send(embed=embed)

    if game.game_in_progress:
        await play_round(ctx)

async def end_game(ctx):
    global game
    embed = discord.Embed(title="Game over! 🏁 Final scores:", color=0x00ff00)
    for player, score in game.get_scores().items():
        embed.add_field(name=player.name, value=score, inline=False)
    await ctx.send(embed=embed)

    winners = game.get_winners()
    if len(winners) == 1:
        await ctx.send(f"The winner is {winners[0].name} with {game.get_scores()[winners[0]]} points! 🏆")
    else:
        winners_names = ", ".join([winner.name for winner in winners])
        await ctx.send(f"It's a tie! The winners are {winners_names} with {game.get_scores()[winners[0]]} points each! 🏆")

    game.reset()
load_dotenv()
bot.run(os.getenv['TOKEN'])
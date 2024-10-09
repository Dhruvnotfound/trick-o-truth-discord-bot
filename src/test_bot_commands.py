import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
import discord

from main import bot, TruthGame

@pytest.fixture
def mock_ctx():
    ctx = MagicMock()
    ctx.guild = MagicMock()
    ctx.author = MagicMock()
    ctx.send = AsyncMock()
    ctx.message = MagicMock()
    ctx.channel = MagicMock()
    ctx.bot = bot
    return ctx

@pytest.fixture
def no_sleep(monkeypatch):
    async def mock_sleep(seconds):
        pass
    monkeypatch.setattr(asyncio, 'sleep', mock_sleep)

@pytest.mark.asyncio
async def test_on_ready():
    with patch('builtins.print') as mock_print:
        with patch.object(bot, 'change_presence') as mock_change_presence:
            await bot.on_ready()
            mock_print.assert_called_once_with(f'{bot.user} has connected to Discord! 🎉')
            mock_change_presence.assert_awaited_once()

@pytest.mark.asyncio
async def test_on_command_error(mock_ctx):
    # Test MissingPermissions error
    error = commands.MissingPermissions(['manage_messages'])
    await bot.on_command_error(mock_ctx, error)
    mock_ctx.send.assert_awaited_with("I don't have the necessary permissions to execute this command. 😢")
    
    mock_ctx.send.reset_mock()

    # Test Forbidden error
    error = discord.Forbidden(MagicMock(), "Forbidden action")
    await bot.on_command_error(mock_ctx, error)
    mock_ctx.send.assert_awaited_with("I'm lacking permissions to perform this action. 😢")
    
    mock_ctx.send.reset_mock()

    # Test other errors
    error = Exception("Unknown error")
    with pytest.raises(Exception):
        await bot.on_command_error(mock_ctx, error)

@pytest.mark.asyncio
async def test_help_command(mock_ctx):
    await bot.get_command('help').callback(mock_ctx)
    mock_ctx.send.assert_awaited()

    # Check if an embed was sent
    sent_args = mock_ctx.send.call_args[1]
    assert 'embed' in sent_args
    embed = sent_args['embed']
    assert isinstance(embed, discord.Embed)
    assert embed.title == "Help 📚"

'''@pytest.mark.asyncio
async def test_start_game(mock_ctx, monkeypatch, no_sleep):
    # Mock the game object
    with patch('main.game', new=TruthGame()):
        game = TruthGame()
        with patch('main.game', game):
            # Mock View and Button interactions
            with patch('discord.ui.View') as mock_view_class:
                mock_view = MagicMock()
                mock_view_class.return_value = mock_view

                # Prepare to capture the 'join_callback' function
                join_callback = None

                # Define a function to capture the join_callback
                def side_effect(item):
                    nonlocal join_callback
                    join_callback = item.callback

                mock_view.add_item.side_effect = side_effect

                # Call the command
                await bot.get_command('start').callback(mock_ctx)

                # Ensure join_callback was captured
                assert join_callback is not None, "join_callback was not captured"

                # Simulate players clicking the join button
                for player_id, player_name in [(1, 'Player1'), (2, 'Player2')]:
                    mock_interaction = MagicMock()
                    mock_interaction.user = MagicMock()
                    mock_interaction.user.name = player_name
                    mock_interaction.user.id = player_id
                    mock_interaction.response = AsyncMock()
                    await join_callback(mock_interaction)

                # Since we've mocked asyncio.sleep, the countdown completes immediately

                # Assert that the expected messages were sent
                mock_ctx.send.assert_any_await(
                    "A new game is starting! Click the button to join! 🕹️",
                    view=mock_view
                )
                mock_ctx.send.assert_any_await(
                    f"Game started with {len(game.players)} players! 🎮 \n check your dms 💌"
                )'''

@pytest.mark.asyncio
async def test_stop_game(mock_ctx):
    # Mock the game object
    with patch('main.game', new=TruthGame()):
        game = TruthGame()
        game.game_in_progress = True

        # Add players and scores
        player1 = MagicMock()
        player1.name = 'Player1'
        player1.id = 1
        game.add_player(player1)
        game.scores[player1] = 10

        player2 = MagicMock()
        player2.name = 'Player2'
        player2.id = 2
        game.add_player(player2)
        game.scores[player2] = 15

        with patch('main.game', game):
            await bot.get_command('stop').callback(mock_ctx)
            mock_ctx.send.assert_any_await("The game has been stopped. 🛑")
            assert game.game_in_progress is False

            # Check that the final scores embed was sent
            embed_sent = False
            for call in mock_ctx.send.await_args_list:
                if 'embed' in call.kwargs:
                    embed = call.kwargs['embed']
                    if isinstance(embed, discord.Embed) and embed.title == "Game over! 🏁 Final scores:":
                        embed_sent = True
                        break
            assert embed_sent, "Final scores embed was not sent"
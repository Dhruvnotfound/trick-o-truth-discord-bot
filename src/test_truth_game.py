import discord
from discord.ext import commands
import pytest
from main import TruthGame

@pytest.fixture
def game():
    #Fixture to create a new TruthGame instance before each test.
    return TruthGame()

def test_init(game):
    #Test the initialization of the game.
    assert game.players == []
    assert game.current_player is None
    assert game.truths == {}
    assert game.scores == {}
    assert game.game_in_progress is False

def test_add_player(game):
    #Test adding players to the game
    player1 = "Player1"
    player2 = "Player2"

    #Add a new player
    assert game.add_player(player1) is True
    assert player1 in game.players
    assert game.scores[player1] == 0

    #Add another new player
    assert game.add_player(player2) is True
    assert player2 in game.players
    assert game.scores[player2] == 0

    #Try adding the same player again
    assert game.add_player(player1) is False
    assert game.players.count(player1) == 1

def test_start_game(game):
    #Game should not start with less than 2 players
    player1 = "Player1"
    game.add_player(player1)
    assert game.start_game() is False
    assert game.game_in_progress is False

    #Game should start with 2 or more players
    player2 = "Player2"
    game.add_player(player2)
    assert game.start_game() is True
    assert game.game_in_progress is True
    assert len(game.players) == 2

def test_stop_game(game):
    #Start the game first
    player1 = "Player1"
    player2 = "Player2"
    game.add_player(player1)
    game.add_player(player2)
    game.start_game()
    assert game.game_in_progress is True

    #Stop the game
    game.stop_game()
    assert game.game_in_progress is False

def test_next_player(game):
    player1 = "Player1"
    player2 = "Player2"
    player3 = "Player3"
    game.add_player(player1)
    game.add_player(player2)
    game.add_player(player3)

    #Start the game
    game.start_game()
    assert game.current_player is None

    #Get the next player
    next_player = game.next_player()
    assert next_player == game.current_player
    assert next_player in game.players

    #Get the second player
    second_player = game.next_player()
    assert second_player == game.current_player
    assert second_player in game.players
    assert second_player != next_player

    #Get the third player
    third_player = game.next_player()
    assert third_player == game.current_player
    assert third_player in game.players
    assert third_player not in [next_player, second_player]

    #No more players, should return None
    assert game.next_player() is None

def test_add_truth(game):
    player = "Player1"
    game.add_player(player)

    #Add a truth
    truth = "I have climbed Mount Everest."
    game.add_truth(player, truth)
    assert game.truths[player] == [truth]

    #Add another truth
    truth2 = "I have a pet snake."
    game.add_truth(player, truth2)
    assert game.truths[player] == [truth, truth2]

def test_get_truths(game):
    player = "Player1"
    game.add_player(player)

    #No truths yet
    assert game.get_truths(player) == []

    #Add truths
    truths = ["I speak four languages.", "I was born on a leap day."]
    for truth in truths:
        game.add_truth(player, truth)

    #Retrieve truths
    retrieved_truths = game.get_truths(player)
    assert retrieved_truths == truths

def test_update_score(game):
    guesser = "Guesser"
    truth_teller = "TruthTeller"
    fake_truth_author = "FakeTruthAuthor"

    game.add_player(guesser)
    game.add_player(truth_teller)
    game.add_player(fake_truth_author)

    #Initial scores should be zero
    assert game.scores[guesser] == 0
    assert game.scores[truth_teller] == 0
    assert game.scores[fake_truth_author] == 0

    #Correct guess
    game.update_score(guesser, truth_teller, None, correct=True)
    assert game.scores[guesser] == 10

    #Incorrect guess, fake truth author gains points
    game.update_score(guesser, truth_teller, fake_truth_author, correct=False)
    assert game.scores[fake_truth_author] == 5

def test_get_scores(game):
    player1 = "Player1"
    player2 = "Player2"
    game.add_player(player1)
    game.add_player(player2)

    #Update scores
    game.scores[player1] = 15
    game.scores[player2] = 10

    scores = game.get_scores()
    assert scores[player1] == 15
    assert scores[player2] == 10

def test_get_winners(game):
    player1 = "Player1"
    player2 = "Player2"
    player3 = "Player3"
    game.add_player(player1)
    game.add_player(player2)
    game.add_player(player3)

    #Set scores
    game.scores[player1] = 20
    game.scores[player2] = 15
    game.scores[player3] = 20

    winners = game.get_winners()
    assert set(winners) == {player1, player3}

def test_reset(game):
    player1 = "Player1"
    game.add_player(player1)
    game.start_game()
    game.add_truth(player1, "I have a dog.")
    game.scores[player1] = 10

    #Reset the game
    game.reset()

    #Check that all attributes are reset
    assert game.players == []
    assert game.current_player is None
    assert game.truths == {}
    assert game.scores == {}
    assert game.game_in_progress is False

from game_logic import HandCricketGame

game = HandCricketGame("Player 1", "Player 2")

# Inning 1
print("\n🏏 Player 1's Innings")
while not game.is_out:
    p1 = int(input("Player 1 (bat): "))
    p2 = int(input("Player 2 (bowl): "))
    game.play_turn(p1, p2)

# Swap
game.swap_roles()

# Inning 2
print("\n🏏 Player 2's Innings")
while not game.is_out and game.scores["Player 2"] <= game.scores["Player 1"]:
    p2 = int(input("Player 2 (bat): "))
    p1 = int(input("Player 1 (bowl): "))
    game.play_turn(p2, p1)

# Result
print("\n🏆 " + game.get_winner())

class HandCricketGame:
    def __init__(self):
        self.scores = {"player1": 0, "player2": 0}
        self.current_batter = "player1"
        self.current_bowler = "player2"
        self.is_out = False
        self.innings = 1

    def play_turn(self, bat, bowl):
        if bat == bowl:
            self.is_out = True
        else:
            self.scores[self.current_batter] += bat

    def swap_roles(self):
        self.current_batter, self.current_bowler = self.current_bowler, self.current_batter
        self.is_out = False
        self.innings += 1

    def is_game_over(self):
        return self.innings > 2

    def get_winner(self):
        s1 = self.scores["player1"]
        s2 = self.scores["player2"]
        if s1 > s2:
            return "Player 1 Wins!"
        elif s2 > s1:
            return "Player 2 Wins!"
        else:
            return "It's a Draw!"

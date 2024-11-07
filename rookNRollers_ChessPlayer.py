from chess_player import ChessPlayer
import random

class rookNRollers_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # YOUR MIND-BOGGLING CODE GOES HERE
        # (random choice for now)
        return random.choice(
            self.board.get_all_available_legal_moves(self.color))
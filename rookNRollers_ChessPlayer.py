from chess_player import ChessPlayer
import random

class rookNRollers_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # YOUR MIND-BOGGLING CODE GOES HERE
        # (random choice for now)
        print("Evaluation before move:", self.eval_function())
        return random.choice(
            self.board.get_all_available_legal_moves(self.color))

    def eval_function(self):
        
		# set opponent's color
        opponent = 'black' if self.color == 'white' else 'white'

        if self.board.is_king_in_checkmate(self.color):
            # if we are in checkmate, return -100
            return -100
        elif self.board.is_king_in_check(self.color):
            # if we are in check, return -20
            return -20
        
        if self.board.is_king_in_checkmate(opponent):
            # if opponent is in checkmate, return 5
            return 5
        elif self.board.is_king_in_check(opponent):
            # if opponent is in check, return 10
            return 10
        
        return 0
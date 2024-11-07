from chess_player import ChessPlayer
import random

class rookNRollers_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # YOUR MIND-BOGGLING CODE GOES HERE
        # (random choice for now)

        print("Evaluation before move:", self.eval_function()) # print board eval score (for testing purposes)

        bestScore = -float('inf') if self.current_player == 'X' else float('inf')
        bestMove = None
        
        # self.board.get_all_available_legal_moves(self.color))
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.current_player
                    score = self.minimax(self.board, 0, self.current_player == 'O')
                    self.board[i][j] = ' '
                    if self.current_player == 'X': # Maximizing
                        if score > bestScore:
                            bestScore = score
                            bestMove = (i, j)
                    else: # Minimizing
                        if score < bestScore:
                            bestScore = score
                            bestMove = (i, j)
        if bestMove:
            self.make_move(bestMove[0], bestMove[1])

    def minimax(self, board, depth, isMaximizing):
        if self.check_winner('X'):
            return 1
        elif self.check_winner('O'):
            return -1
        elif self.is_board_full():
            return 0
        
        if isMaximizing:
            bestScore = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        bestScore = min(score, bestScore)
            return bestScore


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
            return 50
        elif self.board.is_king_in_check(opponent):
            # if opponent is in check, return 10
            return 10
        
        return 0
from chess_player import ChessPlayer
import random
from copy import deepcopy

class rookNRollers_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # YOUR MIND-BOGGLING CODE GOES HERE

        print("Evaluation before move:", self.eval_function(self.board)) # print board eval score (for testing purposes)

        # white is maximizing, black is minimizing
        bestScore = -float('inf') if self.color == 'white' else float('inf')
        bestMove = None

        moves = self.board.get_all_available_legal_moves(self.color)
        for move in moves:

            temp_board = deepcopy(self.board) # make a copy of the current board to use for searching

            temp_board.make_move(move[0], move[1]) # making move
            score = self.minimax(temp_board, 0, self.color == 'black') # get score
            # we don't need to revert move, since we are working on a copy board

            if self.color == 'white': # Maximizing (we are white)
                if score > bestScore:
                    bestScore = score
                    bestMove = move
            else: # Minimizing (we are black)
                if score < bestScore:
                    bestScore = score
                    bestMove = move

        if bestMove: return bestMove # return the best move we found



    """
    Recursive minimax function.
    """
    def minimax(self, board, depth, isMaximizing):

        # hard-coded depth limit of 2:
        if depth == 1:
            return self.eval_function(board)
        
        if isMaximizing:
            bestScore = -float('inf')
            moves = board.get_all_available_legal_moves('white')
            for move in moves:
                temp_board = deepcopy(board) # make a copy of the current board to use for searching
                temp_board.make_move(move[0], move[1]) # making move
                score = self.minimax(temp_board, depth + 1, False)
                bestScore = max(score, bestScore)
            return bestScore
        
        else:
            bestScore = float('inf')
            moves = board.get_all_available_legal_moves('black')
            for move in moves:
                temp_board = deepcopy(board) # make a copy of the current board to use for searching
                temp_board.make_move(move[0], move[1]) # making move
                score = self.minimax(temp_board, depth + 1, True)
                bestScore = min(score, bestScore)
            return bestScore


    """
    Evaluation function. Returns an evaluation score for a given board.
    """
    def eval_function(self, board):
        
        if board.is_king_in_checkmate('white'):
            # if we are in checkmate, return -100
            return -100
        elif board.is_king_in_check('white'):
            # if we are in check, return -20
            return -20
        
        if board.is_king_in_checkmate('black'):
            # if opponent is in checkmate, return 100
            return 100
        elif board.is_king_in_check('black'):
            # if opponent is in check, return 10
            return 10
        
        return 0
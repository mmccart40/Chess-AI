from chess_player import ChessPlayer
import random
from copy import deepcopy
import math

class rookNRollers_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        self.values = {
            # standard pieces
            "P": 1, # white pawn
            "N": 3, # white knight
            "B": 3, # white bishop
            "R": 5, # white rook
            "Q": 10, # white queen
            "K": 1000, # white king
            "p": -1, # black pawn
            "n": -3, # black knight
            "b": -3, # black bishop
            "r": -5, # black rook
            "q": -10, # black queen
            "k": -1000, # black king

            # fake pieces:
            "S" : 6,
            "F" : 2,
            "Y" : 4,
            "s" : -6,
            "f" : -2,
            "y" : -4,
        }
        self.turn = 0

        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # YOUR MIND-BOGGLING CODE GOES HERE

        print("Evaluation before move:", self.eval_function(self.board)) # print board eval score (for testing purposes)
        self.turn += 1

        # white is maximizing, black is minimizing
        bestScore = -float('inf') if self.color == 'white' else float('inf')
        bestMove = None

        moves = self.board.get_all_available_legal_moves(self.color)
        depth_limit = math.floor(20 / len(moves))
        print("depth:", depth_limit)

        for move in moves:

            temp_board = deepcopy(self.board) # make a copy of the current board to use for searching

            temp_board.make_move(move[0], move[1]) # making move
            score = self.minimax(temp_board, 1, self.color == 'black', depth_limit, -float('inf'), float('inf')) # get score
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
    def minimax(self, board, depth, isMaximizing, depth_limit, alpha, beta):

        # hard-coded depth limit:
        if depth >= depth_limit:
            return self.eval_function(board)
        
        if isMaximizing:
            bestScore = -float('inf')
            moves = board.get_all_available_legal_moves('white')
            for move in moves:
                temp_board = deepcopy(board) # make a copy of the current board to use for searching
                temp_board.make_move(move[0], move[1]) # making move
                score = self.minimax(temp_board, depth + 1, False, depth_limit, alpha, beta)
                bestScore = max(score, bestScore)
                if beta <= alpha: break # alpha beta pruning! :)
            return bestScore
        
        else:
            bestScore = float('inf')
            moves = board.get_all_available_legal_moves('black')
            for move in moves:
                temp_board = deepcopy(board) # make a copy of the current board to use for searching
                temp_board.make_move(move[0], move[1]) # making move
                score = self.minimax(temp_board, depth + 1, True, depth_limit, alpha, beta)
                bestScore = min(score, bestScore)
                if beta <= alpha: break # alpha beta pruning! :)
            return bestScore


    """
    Evaluation function. Returns an evaluation score for a given board.
    """
    def eval_function(self, board):

        score = 0

        # --- LOOK FOR CHECK/CHECKMATE --- 3        
        if self.turn > 3:
            if board.is_king_in_check('white'): # if white is in check
                if board.is_king_in_checkmate('white'): return -100 # check for checkmate (-100)
                score -= 1
            
            if board.is_king_in_check('black'): # if black is in check
                if board.is_king_in_checkmate('black'): return 100 # check for checkmate (100)
                score += 1
        # ------- #

        # --- PIECE DIFFERENTIAL --- #
        for loc, piece in board.items():
            # center pawns are good!
            if (piece.get_notation() == 'p' or piece.get_notation() == 'P'):
                if loc[0] > 'c' and loc[0] < 'f':
                    if int(loc[1]) > 3 and int(loc[1]) < 6:
                        score += self.values[piece.get_notation()] * 1.25
                elif loc[0] > 'b' and loc[0] < 'g':
                    if int(loc[1]) > 2 and int(loc[1]) < 7:
                        score += self.values[piece.get_notation()] * 1.1
            # everything else
            else:
                score += self.values[piece.get_notation()]
        # ------- #
        
        return score
from chess_player import ChessPlayer
import random
from copy import deepcopy
import math
from chess_piece import *
import time

class rookNRollers_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        self.turn = 0
        self.last_score = 0
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

        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # YOUR MIND-BOGGLING CODE GOES HERE
        start = time.time()

        self.turn += 1
        print('------------')
        print(self.color, '- turn', self.turn)
        print("Remaining time:", your_remaining_time)
        print("Evaluation before move:", self.eval_function(self.board)) # print board eval score (for testing purposes)

        # white is maximizing, black is minimizing
        bestScore = -float('inf') if self.color == 'white' else float('inf')
        bestMove = None

        moves = self.board.get_all_available_legal_moves(self.color)
        
        opp = 'black' if self.color == 'white' else 'white'
        total_moves = len(moves) + len(self.board.get_all_available_legal_moves(opp))
        print('Total moves:', total_moves)
        if total_moves < 11:
            depth_limit = 6
        elif total_moves < 21:
            depth_limit = 4
        else:
            depth_limit = 2
        
        '''
        pc_count = len(self.board.items())
        print('Piece count:', pc_count)
        
        depth_limit = 2
        if pc_count < 12:
            depth_limit = 4
        if pc_count < 9:
            depth_limit = 6
        '''
        print("depth:", depth_limit)


        for move in moves:
            temp_board = deepcopy(self.board) # make a copy of the current board to use for searching

            temp_board.make_move(move[0], move[1]) # making move
            score = self.minimax(temp_board, 1, self.color == 'black', depth_limit, -float('inf'), float('inf')) # get score

            if self.color == 'white': # Maximizing (we are white)
                if score > bestScore:
                    bestScore = score
                    bestMove = move
            else: # Minimizing (we are black)
                if score < bestScore:
                    bestScore = score
                    bestMove = move

        self.last_score = bestScore

        end = time.time()
        print('Thinking time:', end-start)
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
                alpha = max(bestScore, alpha)
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
                beta = min(bestScore, beta)
                if beta <= alpha: break # alpha beta pruning! :)
            return bestScore


    """
    Evaluation function. Returns an evaluation score for a given board.
    """
    def eval_function(self, board):

        score = 0

        # --- LOOK FOR CHECK/CHECKMATE --- 3        
        if self.turn > 6:
            if board.is_king_in_check('white'): # if white is in check
                if board.is_king_in_checkmate('white'): return -1000 # check for checkmate (-100)
                score -= 0.9
            
            if board.is_king_in_check('black'): # if black is in check
                if board.is_king_in_checkmate('black'): return 1000 # check for checkmate (100)
                score += 0.9
        # ------- #


        # --- PIECE DIFFERENTIAL --- #
        for loc, piece in board.items():
            piece_char = piece.get_notation()
            
            # center pawns are good!
            if (piece_char == 'p' or piece_char == 'P'):
                if loc[0] > 'c' and loc[0] < 'f':
                    if int(loc[1]) > 3 and int(loc[1]) < 6:
                        score += self.values[piece_char] * 1.01
                elif loc[0] > 'b' and loc[0] < 'g':
                    if int(loc[1]) > 2 and int(loc[1]) < 7:
                        score += self.values[piece_char] * 1.005
                else:
                    score += self.values[piece_char]
            # king moves are not ideal
            elif piece_char.lower() == 'k':
                score += self.values[piece_char] * 0.99
            else:
                score += self.values[piece_char]
        # ------- #

        
        # --- ATTACKED VS ATTACKING --- #
        '''
        for item in board.items():
            loc, piece = item
            piece_char = piece.get_notation()
            if (piece_char.lower() == 'p'): # skip pawns
                continue
            if (piece_char.lower() == 'n'): # skip knights
                continue
            if (piece_char.lower() == 'b'): # skip bishops
                continue
            if (piece_char.lower() == 'k'): # skip kings (checks are handled earlier)
                continue
            if self.is_piece_attacked(item):
                score += self.values[piece_char] * -0.1 # attacking is slightly good, being attacked is slightly bad
        '''
        # ------- #
        
        return score
    
    def is_piece_attacked(self, item):
        '''Return True if the player whose color is passed is currently attacked'''
        color = 'white' if item[1].get_notation().isupper() else 'black'
        loc = item[0]
        return loc in [ loc for _,loc in self.board._get_all_available_moves(
            'white' if color=='black' else 'black')]
    
    def get_piece_at_loc(self, board, location):
        for loc, piece in board.items():
            if location == loc:
                return piece
        return False
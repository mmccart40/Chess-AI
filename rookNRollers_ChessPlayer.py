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
            depth_limit = 4
        elif total_moves < 21:
            depth_limit = 3
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
                elif score == bestScore and random.random() < .2:
                    bestScore = score
                    bestMove = move

            else: # Minimizing (we are black)
                if score < bestScore:
                    bestScore = score
                    bestMove = move
                elif score == bestScore and random.random() < .2:
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
                score -= 0.005
            
            if board.is_king_in_check('black'): # if black is in check
                if board.is_king_in_checkmate('black'): return 1000 # check for checkmate (100)
                score += 0.005
        # ------- #


        # --- PIECE DIFFERENTIAL --- #
        for loc, piece in board.items():
            piece_char = piece.get_notation()
            
            # center pawn bonus!
            if (piece_char.lower() == 'p'):
                sign = 1 if piece_char == 'P' else -1 # white = positive, black = negative
                if loc[0] > 'c' and loc[0] < 'f':
                    if int(loc[1]) > 3 and int(loc[1]) < 6:
                        score += sign * 0.015
                elif loc[0] > 'b' and loc[0] < 'g':
                    if int(loc[1]) > 2 and int(loc[1]) < 7:
                        score += sign * 0.01
            # center knight bonus!
            #elif (piece_char.lower() == 'n'):
            #    sign = 1 if piece_char == 'N' else -1 # white = positive, black = negative
            #    if loc[0] > 'b' and loc[0] < 'g':
            #        if int(loc[1]) > 2 and int(loc[1]) < 7:
            #            score += sign * 0.001
            # sedentary knight/bishop penalty
            if (piece_char.lower() == 'n' or piece_char.lower() == 'b'):
                if (piece_char == 'N' or piece_char == 'B'): # white
                    if (int(loc[1]) == 1):
                        score -= .01
                else: # black
                    if (int(loc[1]) == 8):
                        score += .01
            # active rook bonus!
            elif (piece_char.lower() == 'r'):
                sign = 1 if piece_char == 'R' else -1 # white = positive, black = negative
                if loc[0] > 'c' and loc[0] < 'f':
                    score += sign * .2
            
            # standard piece value
            score += self.values[piece_char]
        # ------- #

        white_moves = board._get_all_available_moves('white')
        black_moves = board._get_all_available_moves('black')

        # --- ATTACKING --- #
        for item in board.items():
            loc, piece = item
            piece_char = piece.get_notation()
            if (piece_char.lower() == 'k'): # skip kings (checks are handled earlier)
                continue
            if self.is_piece_attacked(item, white_moves, black_moves):
                score += self.values[piece_char] * -0.005 # attacking is slightly good, being attacked is slightly bad
        # ------- #

        # --- DEFENDING --- #
        for item in board.items():
            loc, piece = item
            piece_char = piece.get_notation()
            if (piece_char.lower() == 'k'): # skip kings
                continue
            if self.is_piece_defended(item, white_moves, black_moves):
                score += self.values[piece_char] * 0.005 # defeding pieces is good
        # ------- #
        
        return score
    
    # helper functions

    def is_piece_attacked(self, item, white_moves, black_moves):
        '''Return True if the piece is currently attacked'''
        color = 'white' if item[1].get_notation().isupper() else 'black'
        loc = item[0]
        return loc in [ loc for _,loc in (black_moves if color=='white' else white_moves)]
    
    def is_piece_defended(self, item, white_moves, black_moves):
        '''Return True if the piece is currently defended'''
        color = 'white' if item[1].get_notation().isupper() else 'black'
        loc = item[0]
        return loc in [ loc for _,loc in (white_moves if color=='white' else black_moves)]
    
    def get_piece_at_loc(self, board, location):
        for loc, piece in board.items():
            if location == loc:
                return piece
        return False
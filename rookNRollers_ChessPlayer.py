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
        self.looking_to_castle = True
        self.prune_count = 0
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
        print(self.color, '- turn', self.turn)
        print("Remaining time:", your_remaining_time)
        print("Evaluation before move:", self.eval_function(self.board)) # print board eval score (for testing purposes)

        # white is maximizing, black is minimizing
        bestScore = -float('inf') if self.color == 'white' else float('inf')
        bestMove = None

        moves = self.board.get_all_available_legal_moves(self.color)
        #moves, num_captures = self.sort_moves(moves)
        moves = self.sort_moves_2(moves, self.color, self.board)

        opp = 'black' if self.color == 'white' else 'white'
        total_moves = len(moves) + len(self.board.get_all_available_legal_moves(opp))
        print('Total moves:', total_moves)
        
        depth_limit = 2 if total_moves < 30 else 1
        print("depth:", depth_limit)
        #print('Possible captures:', num_captures)

        count = 0
        for move in moves:
            count += 1
            print("branch:", count)
            temp_board = deepcopy(self.board) # make a copy of the current board to use for searching

            temp_board.make_move(move[0], move[1]) # making move
            score = self.minimax(temp_board, 0, self.color == 'black', depth_limit, -float('inf'), float('inf')) # get score

            if self.color == 'white': # Maximizing (we are white)
                if score > bestScore:
                    bestScore = score
                    bestMove = move
                elif score == bestScore and random.random() < .5:
                    bestScore = score
                    bestMove = move

            else: # Minimizing (we are black)
                if score < bestScore:
                    bestScore = score
                    bestMove = move
                elif score == bestScore and random.random() < .5:
                    bestScore = score
                    bestMove = move

        self.last_score = bestScore

        end = time.time()
        print('Thinking time:', end-start)
        print('Prune count:', self.prune_count)
        print('\n------------\n')
        self.prune_count = 0
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
            #moves = self.sort_moves_2(moves, 'white', board)
            for move in moves:
                
                '''
                # make move, avoiding deepcopy when possible
                #if (not (self.is_piece_at_loc(board, move[1]) or move[0] == board.get_king_location('white'))):
                if (not (self.is_piece_at_loc(board, move[1]) or move[0] == board.get_king_location('white')
                         or move[1][1] == '8' )):
                    # non-captures or non-king moves
                    board[move[0]]._move_yourself(move[0], move[1], board) # make move
                    score = self.minimax(board, depth + 1, False, depth_limit, alpha, beta)
                    board[move[1]]._move_yourself(move[1], move[0], board) # revers move
                else:
                    # captures or king moves
                    temp_board = deepcopy(board) # make a copy of the current board to use for searching
                    temp_board.make_move(move[0], move[1]) # making move
                    score = self.minimax(temp_board, depth + 1, False, depth_limit, alpha, beta)
                '''
                temp_board = deepcopy(board) # make a copy of the current board to use for searching
                temp_board.make_move(move[0], move[1]) # making move
                score = self.minimax(temp_board, depth + 1, False, depth_limit, alpha, beta)
                
                bestScore = max(score, bestScore)
                alpha = max(bestScore, alpha)
                if beta <= alpha:
                    self.prune_count += 1
                    break # alpha beta pruning! :)
            return bestScore
        
        else:
            bestScore = float('inf')
            moves = board.get_all_available_legal_moves('black')
            #moves = self.sort_moves_2(moves, 'black', board)
            for move in moves:

                '''
                # make move, avoiding deepcopy when possible
                if (not (self.is_piece_at_loc(board, move[1]) or move[0] == board.get_king_location('black')
                         or move[1][1] == '1' )):
                #if (not (self.is_piece_at_loc(board, move[1]) or move[0] == board.get_king_location('black')) ):
                    # non-captures or non-king moves
                    board[move[0]]._move_yourself(move[0], move[1], board) # make move
                    score = self.minimax(board, depth + 1, True, depth_limit, alpha, beta)
                    board[move[1]]._move_yourself(move[1], move[0], board) # revers move
                else:
                    # captures or king moves
                    temp_board = deepcopy(board) # make a copy of the current board to use for searching
                    temp_board.make_move(move[0], move[1]) # making move
                    score = self.minimax(temp_board, depth + 1, True, depth_limit, alpha, beta)
                '''
                temp_board = deepcopy(board) # make a copy of the current board to use for searching
                temp_board.make_move(move[0], move[1]) # making move
                score = self.minimax(temp_board, depth + 1, True, depth_limit, alpha, beta)
                
                bestScore = min(score, bestScore)
                beta = min(bestScore, beta)
                if beta <= alpha:
                    self.prune_count += 1
                    break # alpha beta pruning! :)
            return bestScore


    """ Evaluation function. Returns an evaluation score for a given board. """
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

        
        ''' this is pretty slow
        # --- STALEMATE --- #
        if (board._is_stalemated('white') or board._is_stalemated('black')):
            return 0
        # ------- #
        '''

        
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
            # sedentary knight/bishop penalty
            if (piece_char.lower() == 'n' or piece_char.lower() == 'b'):
                if (piece_char == 'N' or piece_char == 'B'): # white
                    if (int(loc[1]) == 1):
                        score -= .012
                else: # black
                    if (int(loc[1]) == 8):
                        score += .012
            # active rook bonus!
            elif (piece_char.lower() == 'r' and self.looking_to_castle):
                sign = 1 if piece_char == 'R' else -1 # white = positive, black = negative
                if loc[0] > 'c' and loc[0] < 'g':
                    score += sign * .2
                    self.looking_to_castle = False
            
            # standard piece value
            score += self.values[piece_char]
        # ------- #
        
        #'''
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
        #'''
        
        return score
    


    # --- HELPER FUNCTIONS --- #

    ''' Sorts moves by prioritizing captures '''
    def sort_moves(self, moves):
        sorted_moves = []
        num_captures = 0
        for move in moves:
            if (self.is_piece_at_loc(self.board, move[1])): # piece
                sorted_moves.insert(0, move)
                num_captures += 1
            else: # no piece
                sorted_moves.append(move)
        return sorted_moves, num_captures

    ''' Sorts move based on evaluation function '''
    def sort_moves_2(self, moves, color, board):
        sorted_moves = []
        dict = {}
        for move in moves:
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            dict[move] = self.eval_function(temp_board) # score : move
        if color == 'white':
            while len(dict) > 0:
                maxi = -99999
                for move in dict.keys():
                    if dict[move] > maxi:
                        maxi = dict[move]
                        best_move = move
                sorted_moves.append(best_move)
                dict.pop(best_move)
        else:
            while len(dict) > 0:
                mini = 99999
                for move in dict.keys():
                    if dict[move] < mini:
                        mini = dict[move]
                        best_move = move
                sorted_moves.append(best_move)
                dict.pop(best_move)
        return sorted_moves
    

    ''' Return True if the piece is currently attacked '''
    def is_piece_attacked(self, item, white_moves, black_moves):
        color = 'white' if item[1].get_notation().isupper() else 'black'
        loc = item[0]
        return loc in [ loc for _,loc in (black_moves if color=='white' else white_moves)]
    
    ''' Return True if the piece is currently defended '''
    def is_piece_defended(self, item, white_moves, black_moves):
        color = 'white' if item[1].get_notation().isupper() else 'black'
        loc = item[0]
        return loc in [ loc for _,loc in (white_moves if color=='white' else black_moves)]
    
    ''' Return True if there is a piece at the given location '''
    def is_piece_at_loc(self, board, location):
        for loc, piece in board.items():
            if location == loc:
                return True
        return False
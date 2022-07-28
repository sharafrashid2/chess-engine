from chess import board
from chess.board import Board
from chess.constants import ROWS, COLS
from .scores import white_pawn_scores, black_pawn_scores, knight_scores, white_rook_scores, black_rook_scores, white_bishop_scores, black_bishop_scores, white_king_scores, black_king_scores, queen_scores
from .pieces import Pawn, Rook, Bishop, Knight, Queen, King

# This file contains all the functions for calculating the computer's next move

def get_piece_value(piece):
    """
    This function calculates the score for a specific piece based off the piece it is and its position on the board.
    """
    if piece == 0:
        return 0
    
    def get_absolute_value(piece):
        if type(piece) == Pawn:
            if piece.color == 'white':
                return 10 + white_pawn_scores[piece.row][piece.col]
            else:
                return 10 + black_pawn_scores[piece.row][piece.col]
        
        elif type(piece) == Rook:
            if piece.color == 'white':
                return 50 + white_rook_scores[piece.row][piece.col]
            else:
                return 50 + black_rook_scores[piece.row][piece.col]
        
        elif type(piece) == Knight:
            return 30 + knight_scores[piece.row][piece.col]

        elif type(piece) == Bishop:
            if piece.color == 'white':
                return 30 + white_bishop_scores[piece.row][piece.col]
            else:
                return 30 + black_bishop_scores[piece.row][piece.col]

        elif type(piece) == Queen:
            return 90 + queen_scores[piece.row][piece.col]

        elif type(piece) == King:
            if piece.color == 'white':
                return 900 + white_king_scores[piece.row][piece.col]
            else:
                return 900 + black_king_scores[piece.row][piece.col]
    
    absolute_value = get_absolute_value(piece)

    return -absolute_value if piece.color == 'white' else absolute_value

def evaluate_board(board):
    """
    This is a helper function for evaluating the total score of a board based off the pieces currently on it
    and their positions.
    """
    total = 0

    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            total += get_piece_value(piece)
    
    return total

def switch_turn(current):
    if current == 'white':
        return 'black'
    return 'white'

def construct_decision_tree(start_board, start_black_pieces, start_white_pieces, game, deepest_level):
    """
    This function constructs the game's decision tree given the current board state, and you can choose
    how deep you would like the decision tree to go with the parameter deepest_level.
    """
    tree = {}
    def build(tree, turn, start_board, start_black_pieces, start_white_pieces, game, level):

        if level == deepest_level:
            return 

        # build tree base
        if turn == 'black':
            pieces = start_black_pieces
        else:
            pieces = start_white_pieces
        
        for piece in pieces:
            piece.get_all_moves(start_board)
        
        if turn == 'black':
            game.generate_legal_moves(pieces, start_board, False)
        else:
            game.generate_legal_moves(pieces, start_board, False)

        for piece in pieces:
            for move in piece.possible_moves:
                board, black_pieces, white_pieces, black_king, white_king = game.perform_test_move(start_board, piece, move[0], move[1], False)
                score = evaluate_board(board)
                key = ((piece.row, piece.col), move)
                tree[key] = [score, board, black_pieces, white_pieces, {}]
                build(tree[key][4], switch_turn(turn), board, black_pieces, white_pieces, game, level + 1)
    
    build(tree, 'black', start_board, start_black_pieces, start_white_pieces, game, 0)
    return tree


def mini_max(tree, deepest_level):
    """
    This is the main algorithm (mini-max) for finding which move is the best. The algorithm does so by doing a depth
    first search for the highest sum of game board scores on the game's current decision tree up to a specified level, 
    and then returns the starting node that is associated with that highest score. This returned node would be the 
    move that the computer makes.
    """
    start = []
    def traverse(tree, depth, turn, alpha, beta):
        if depth == deepest_level:
            return 0
        
        if turn == 'black':
            max_score = float('-inf')
        else:
            min_score = float('inf')

        for key in tree:
            score = tree[key][0] + traverse(tree[key][4], depth+1, switch_turn(turn), alpha, beta)
            if turn == 'black' and score > max_score:
                max_score = score
                alpha = max(alpha, max_score)

                if depth == 0:
                    if len(start) > 0:
                        start.pop(0)
                    start.append(key)

                if beta <= alpha:
                    break
        
            elif turn == 'white' and score < min_score:
                min_score = score
                beta = min(min_score, beta)

                if depth == 0:
                    if len(start) > 0:
                        start.pop(0)
                    start.append(key)
                
                if beta <= alpha:
                    break
                
        return max_score if turn == 'black' else min_score

    total = traverse(tree, 0, 'black', -float('inf'), float('inf'))
    
    return start[0], total if start else None

        

            
            

    




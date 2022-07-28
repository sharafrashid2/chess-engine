from chess import board
from chess.board import Board
from chess.constants import ROWS, COLS
from .scores import white_pawn_scores, black_pawn_scores, knight_scores, white_rook_scores, black_rook_scores, white_bishop_scores, black_bishop_scores, white_king_scores, black_king_scores, queen_scores
from .pieces import Pawn, Rook, Bishop, Knight, Queen, King


def get_piece_value(piece):
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
    start = []
    def traverse(tree, depth, turn):
        if depth == deepest_level:
            return 0
        
        if turn == 'black':
            max_score = float('-inf')
        else:
            min_score = float('inf')

        for key in tree:
            score = tree[key][0] + traverse(tree[key][4], depth+1, switch_turn(turn))
            if turn == 'black' and score > max_score:
                max_score = score
                if depth == 0:
                    if len(start) > 0:
                        start.pop(0)
                    start.append(key)
            elif turn == 'white' and score < min_score:
                min_score = score
                if depth == 0:
                    if len(start) > 0:
                        start.pop(0)
                    start.append(key)

        return max_score if turn == 'black' else min_score

    total = traverse(tree, 0, 'black')
    
    return start[0], total

        

            
            

    




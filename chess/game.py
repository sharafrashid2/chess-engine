import pygame

from chess.board import Board
from .pieces import Pawn, Queen, Rook, Bishop, Knight, King
from .constants import BLUE, COLS, RED, ROWS, SQUARE_SIZE, MENU_HEIGHT, LIGHT_BROWN, WIDTH, BLACK, PURPLE
from chess.computer_ai import evaluate_board, get_piece_value, construct_decision_tree, mini_max


class Game:
    def __init__(self, win):
        self.win = win
        self._init()
    
    def update(self):
        """
        Function that updates game states, plays for the computer, and redraws changes to the game on
        the graphical user interface.
        """
        self.board.draw()

        if self.promotion and self.turn == 'white':
            # rook promotion box
            pygame.draw.rect(self.win, LIGHT_BROWN, (20 + (WIDTH-60)/5, 10, (WIDTH-60)/5, MENU_HEIGHT-20))
            self.win.blit(self.board.font.render('Rook', True, BLACK), (55 + (WIDTH-60)/5, 15))
            # knight promotion box
            pygame.draw.rect(self.win, LIGHT_BROWN, (30 + 2 * (WIDTH-60)/5, 10, (WIDTH-60)/5, MENU_HEIGHT-20))
            self.win.blit(self.board.font.render('Knight', True, BLACK), (60 + 2 * (WIDTH-60)/5, 15))
            # bishop promotion box
            pygame.draw.rect(self.win, LIGHT_BROWN, (40 + 3 * (WIDTH-60)/5, 10, (WIDTH-60)/5, MENU_HEIGHT-20))
            self.win.blit(self.board.font.render('Bishop', True, BLACK), (70 + 3 * (WIDTH-60)/5, 15))
            # queen promotion box
            pygame.draw.rect(self.win, LIGHT_BROWN, (50 + 4 * (WIDTH-60)/5, 10, (WIDTH-60)/5, MENU_HEIGHT-20))
            self.win.blit(self.board.font.render('Queen', True, BLACK), (80 + 4 * (WIDTH-60)/5, 15))
        
        if self.promotion and self.turn == 'black':
            self.promote_pawn(Queen, *self.promote_unit)
            self.promotion = False
            self.promote_unit = None
            self.go_next_turn()
        
        # updates states in the game once a new turn starts based off the new board
        if self.changed_turn:
            self.generate_all_moves()
            self.threat_map = self.generate_threat_map(self.board.board, self.board.black_pieces, self.board.white_pieces)

            if self.turn == 'white':
                pieces = self.board.white_pieces
            else:
                pieces = self.board.black_pieces

            self.all_legal_moves = self.generate_legal_moves(pieces, self.board.board, self.board.used_jump_two_prev)
            self.changed_turn = False

            self.is_check()
            self.is_checkmate(self.all_legal_moves)
            self.is_stalemate(self.all_legal_moves)

            # here computer makes decisions for black
            if not self.checkmated and not self.stalemated and self.turn == 'black':
                tree = construct_decision_tree(self.board.board, self.board.black_pieces, self.board.white_pieces, self, 3)
                result, total = mini_max(tree, 3)
                if result:
                    self.select(*result[0])
                    self.select(*result[1])

        # displays check text
        if self.checked and not self.checkmated and not self.stalemated:
            pygame.draw.circle(self.win, RED, (self.king[1] * SQUARE_SIZE + SQUARE_SIZE//2, self.king[0] * SQUARE_SIZE + SQUARE_SIZE//2 + MENU_HEIGHT,), 10)
            self.win.blit(self.board.font.render("You are checked!", True, BLACK), (20 + (WIDTH-60)/5, 15))

         # displays checkmate text
        if self.checkmated and self.turn == 'white':
            self.win.blit(self.board.font.render("Checkmate! Black wins.", True, BLACK), (20 + (WIDTH-60)/5, 15))

        elif self.checkmated and self.turn == 'black':
            self.win.blit(self.board.font.render("Checkmate! White wins.", True, BLACK), (20 + (WIDTH-60)/5, 15))

        # displays stalemate text
        elif self.stalemated:
            self.win.blit(self.board.font.render("Stalemate! The game is a draw.", True, BLACK), (20 + (WIDTH-60)/5, 15))
            
        # you can uncomment the following code to see enemy's threat squares each turn
        # for coord in self.threat_map:
        #     row, col = coord
        #     pygame.draw.circle(self.win, PURPLE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2 + MENU_HEIGHT,), 10) 

        self.draw_valid_moves(self.piece_valid_moves)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board(self.win)
        self.turn = "white"
        self.piece_valid_moves = set()
        self.all_legal_moves = set()
        self.changed_turn = True
        self.king = None
        self.checked = False
        self.checkmated = False
        self.stalemated = False
        self.threat_map = set()
        
        # pawn edge case booleans
        self.promotion = False
        self.promote_unit = None

    def reset(self):
        self._init()
    
    def select(self, row, col):
        """
        There are two stages to the select function. The first time you use it, you select a specific piece you want to move. YOu
        then use the select function again to select the square you want the piece to move to.
        """
        if self.checkmated or self.stalemated:
            return
        
        piece = self.board.get_piece(row, col)

        if (not self.selected and piece != 0 and piece.color == self.turn) or (self.selected and piece != 0 and piece.color == self.turn):
            self.selected = self.board.get_piece(row, col)
            self.piece_valid_moves = piece.possible_moves
            return

        elif piece == 0 or piece.color != self.turn:
            if piece != 0 and (row, col) in self.piece_valid_moves:
                if self.turn == "white":
                    self.board.black_pieces.remove(piece)
                else:
                    self.board.white_pieces.remove(piece)

                self.board.board[piece.row][piece.col] = 0
            if type(self.selected) == Pawn or type(self.selected) == King:
                prev = (self.selected.row, self.selected.col)
            moved = self._move(row, col)

            # Here we handle edge cases that arise from special moves in the game
            if moved:
                 # rook and king case so castle can no longer happen
                if (type(self.selected) == Rook or type(self.selected) == King) and not self.selected.moved:
                    self.selected.moved = True
                
                # castling cases
                if type(self.selected) == King and (self.selected.col - prev[1] == 2):
                    piece = self.board.get_piece(self.selected.row, COLS-1)
                    piece.col = self.selected.col - 1
                    piece.calc_pos()
                    self.board.board[self.selected.row][COLS-1] = 0
                    self.board.board[self.selected.row][piece.col] = piece

                if type(self.selected) == King and self.selected.col - prev[1] == -2:
                    piece = self.board.get_piece(self.selected.row, 0)
                    piece.col = self.selected.col + 1
                    piece.calc_pos()
                    self.board.board[self.selected.row][0] = 0
                    self.board.board[self.selected.row][piece.col] = piece

                # pawn promotion edge case
                if (
                    type(self.selected) == Pawn and ((self.selected.color == 'white' and self.selected.row == 0) or
                    (self.selected.color == 'black' and self.selected.row == 7))
                ):
                    self.promotion = True
                    self.promote_unit = (row, col)
                    self.piece_valid_moves = set()
                    return 
                
                # pawn en passe susceptible case
                if (
                    type(self.selected) == Pawn and abs(prev[0] - row) == 2
                ):
                    self.board.used_jump_two_prev = [True, 0, self.selected]
                
                # pawn en passe occurs case
                test = self.board.used_jump_two_prev
                if (
                    type(self.selected) == Pawn and test and
                    test[1] == 1 and abs(self.selected.row - test[2].row) == 1 and
                    self.selected.col == test[2].col
                ):
                    to_remove = test[2]
                    self.board.board[to_remove.row][to_remove.col] = 0

                    if self.turn == "white":
                        self.board.black_pieces.remove(to_remove)
                    else:
                        self.board.white_pieces.remove(to_remove)

                if self.board.used_jump_two_prev != False and self.board.used_jump_two_prev[1] == 1:
                    self.board.used_jump_two_prev = False

                self.go_next_turn()

                if self.board.used_jump_two_prev != False and self.board.used_jump_two_prev[1] == 0:
                    self.board.used_jump_two_prev[1] += 1
            else:
                self.changed_turn = False
                self.selected = None
                self.piece_valid_moves = set()
    
    def _move(self, row, col):
        """
        Helper function for updating a piece's location and also changing its position on the game's board.
        """
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.piece_valid_moves:
            self.board.move(self.selected, row, col)
        else:
            return False
        return True
    
    def is_check(self):
        """
        Checks the game to see if a side is checked.
        """
        if self.turn == 'white':
            to_check = self.board.white_pieces
        else:
            to_check = self.board.black_pieces

        for piece in to_check:
            if type(piece) == King and (piece.row, piece.col) in self.threat_map:
                self.checked = True
                self.king = (piece.row, piece.col)
                return True
        
        return False
    
    def is_checkmate(self, all_legal_moves):
        """
        Checks the game to see if there is a checkmate.
        """
        if self.checked and len(all_legal_moves) == 0:
            self.checkmated = True
            return True
        return False
    
    def is_stalemate(self, all_legal_moves):
        """
        Checks the game to see if there is a stalemate.
        """
        if not self.checked and len(all_legal_moves) == 0:
            self.stalemated = True
            return True
        return False
    
    def promote_pawn(self, new_class, row, col):
        """
        Function for promoting a pawn to either a rook, bishop, knight, or queen when it reaches the other
        side of the board.
        """
        if self.turn == 'white':
            self.board.white_pieces.remove(self.board.get_piece(row, col))
            if new_class == Rook:
                self.board.board[row][col] = new_class(row, col, self.selected.color, self.win, True)
            else:
                self.board.board[row][col] = new_class(row, col, self.selected.color, self.win)
            self.board.white_pieces.append(self.board.get_piece(row, col))
        else:
            self.board.black_pieces.remove(self.board.get_piece(row, col))
            if new_class == Rook:
                self.board.board[row][col] = new_class(row, col, self.selected.color, self.win, True)
            else:
                self.board.board[row][col] = new_class(row, col, self.selected.color, self.win)
            self.board.black_pieces.append(self.board.get_piece(row, col))

    
    def draw_valid_moves(self, moves):
        """
        Function that draws blue dots of all the squares a piece can move to when you click on it.
        """
        for move in moves:
            row, col = move
            piece = self.board.get_piece(row, col)
            if piece != 0:
                pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2 + MENU_HEIGHT,), 10)   
            else:
                pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2 + MENU_HEIGHT,), 10)
    
    def go_next_turn(self):
        """
        Helper function that updates the states of the game so that it is now a new turn.
        """
        self.change_turn()
        self.changed_turn = True
        self.selected = None
        self.checked = False
        self.king = None
        self.piece_valid_moves = set()
    
    def generate_all_moves(self):
        """
        Helper function that generates for each piece, all moves (legal or not) that can be made. The results of this
        function are used as a starting point to create a list of all legal moves.
        """
        all_moves = set()
        if self.turn == 'white':
            for piece in self.board.white_pieces:
                if type(piece) == Pawn:
                    all_moves.update(piece.get_all_moves(self.board.board, used_jump_two_prev=self.board.used_jump_two_prev))
                else:
                    all_moves.update(piece.get_all_moves(self.board.board))
        else:
            for piece in self.board.black_pieces:
                if type(piece) == Pawn:
                    all_moves.update(piece.get_all_moves(self.board.board, used_jump_two_prev=self.board.used_jump_two_prev))
                else:
                    all_moves.update(piece.get_all_moves(self.board.board))

        return all_moves
    
    def generate_threat_map(self, board, black_pieces, white_pieces):
        """
        Helper function that generates all squares that are under attack by the opposing side.
        """
        threats = set()
        if self.turn == 'white':
            to_check = black_pieces
        else:
            to_check = white_pieces

        for piece in to_check:
            threats.update(piece.get_threat_spots(board))
        
        return threats
    

    def generate_legal_moves(self, pieces, board, used_jump_two_prev):
        """
        Helper function that generates for each piece, all the legal moves that piece can make.
        """
        all_legal_moves = set()
        # if self.turn == 'white':
        #     pieces = self.board.white_pieces
        # else:
        #     pieces = self.board.black_pieces
        for piece in pieces:
            current = set()
            for move in piece.possible_moves:

                clone_board, clone_black_pieces, clone_white_pieces, clone_black_king, clone_white_king = self.perform_test_move(board, piece, move[0], move[1], used_jump_two_prev)

                test_threatmap = self.generate_threat_map(clone_board, clone_black_pieces, clone_white_pieces)

                # if your king is not in check, then the move is valid
                if piece.color == 'black' and type(piece) != King:
                    if (clone_black_king.row, clone_black_king.col) not in test_threatmap:
                        current.add(move)
                elif type(piece) != King:
                    if (clone_white_king.row, clone_white_king.col) not in test_threatmap:
                        current.add(move)
                else:
                    # print(piece, test_threatmap, (move[0], move[1]))
                    if (move[0], move[1]) not in test_threatmap:
                        current.add(move)
            
            all_legal_moves.update(current)
            piece.possible_moves = current

        return all_legal_moves
    
    def perform_test_move(self, board, piece, move_row, move_col, used_jump_two_prev):
        """
        Helper function for temporarily testing out a move that a piece can make.
        """
        clone_board = []
        clone_white_pieces = []
        clone_black_pieces = []

        # clones board to test move out
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                curr = board[r][c]
                if curr == 0:
                    row.append(0)
                elif curr.name == 'pawn':
                    row.append(Pawn(curr.row, curr.col, curr.color, curr.win, curr.jump_two))
                elif curr.name == 'rook':
                    row.append(Rook(curr.row, curr.col, curr.color, curr.win, curr.moved))
                elif curr.name == 'knight':
                    row.append(Knight(curr.row, curr.col, curr.color, curr.win))
                elif curr.name == 'bishop':
                    row.append(Bishop(curr.row, curr.col, curr.color, curr.win))
                elif curr.name == 'queen':
                    row.append(Queen(curr.row, curr.col, curr.color, curr.win))
                elif curr.name == 'king':
                    row.append(King(curr.row, curr.col, curr.color, curr.win, curr.moved))
            clone_board.append(row)
        
        # clones pieces as well so the actual game isn't interfered with
        for r in range(ROWS):
            for c in range(COLS):
                if clone_board[r][c] != 0 and clone_board[r][c].color == 'white':
                    clone_white_pieces.append(clone_board[r][c])
                    if type(clone_board[r][c]) == King:
                        clone_white_king = clone_board[r][c]
                elif clone_board[r][c] != 0:
                    clone_black_pieces.append(clone_board[r][c])
                    if type(clone_board[r][c]) == King:
                        clone_black_king = clone_board[r][c]

        
        # carries out move to see if king will be put in check after it
        temp = clone_board[piece.row][piece.col]
        prev = (temp.row, temp.col)
        temp.row, temp.col = move_row, move_col
        check_remove = clone_board[move_row][move_col]
        if check_remove != 0 and piece.color == 'white':
            clone_black_pieces.remove(check_remove)
        elif check_remove != 0:
            clone_white_pieces.remove(check_remove)
        clone_board[piece.row][piece.col] = 0
        clone_board[move_row][move_col] = temp

        # en passe case
        test = used_jump_two_prev
        if test:
            test = [test[0], test[1], Pawn(test[2].row, test[2].col, test[2].color, test[2].win, test[2].jump_two)]
        if (
            type(temp) == Pawn and test and
            test[1] == 1 and abs(temp.row - test[2].row) == 1 and
            temp.col == test[2].col
        ):
            clone_board[test[2].row][test[2].col] = 0

            if piece.color == "white":
                for item in clone_black_pieces:
                    if item.row == test[2].row and item.col == test[2].col:
                        to_remove = item
                clone_black_pieces.remove(to_remove)
            else:
                for item in clone_white_pieces:
                    if item.row == test[2].row and item.col == test[2].col:
                        to_remove = item
                clone_white_pieces.remove(to_remove)

        # castling case
        if type(temp) == King and (move_col - prev[1] == 2):
            piece = clone_board[temp.row][COLS-1]
            piece.col = temp.col - 1
            clone_board[temp.row][COLS-1] = 0
            clone_board[temp.row][piece.col] = piece

        if type(temp) == King and move_col - prev[1] == -2:
            piece = clone_board[temp.row][0]
            piece.col = temp.col + 1
            clone_board[temp.row][0] = 0
            clone_board[temp.row][piece.col] = piece
        
        return clone_board, clone_black_pieces, clone_white_pieces, clone_black_king, clone_white_king

    def change_turn(self):
        if self.turn == "black":
            self.turn = "white"
        else:
            self.turn = "black"
    


        



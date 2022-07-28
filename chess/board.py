import pygame
from .pieces import Pawn, Rook, Queen, King, Bishop, Knight
from .constants import BLACK, DARK_GREEN, LIGHT_GREEN, ROWS, COLS, SQUARE_SIZE, BROWN, WIDTH, MENU_HEIGHT, LIGHT_BROWN
from pygame.locals import *

def place_piece(row, col, color, win):
    piece_order = [
                    Rook(row, col, color, win, False), Knight(row, col, color, win), Bishop(row, col, color, win), Queen(row, col, color, win), 
                    King(row, col, color, win, False), Bishop(row, col, color, win), Knight(row, col, color, win), Rook(row, col, color, win, False),
                  ]

    return piece_order[col]

class Board:
    def __init__(self, win):
        self.board = []
        self.font = pygame.font.SysFont('Arial', 17)
        self.black_pieces = []
        self.white_pieces = []
        self.used_jump_two_prev = False
        self.win = win
        self.create_board()

    def draw_squares(self):
        self.win.fill(DARK_GREEN)
        pygame.draw.rect(self.win, BROWN, (0, 0, WIDTH, MENU_HEIGHT ))
        pygame.draw.rect(self.win, LIGHT_BROWN, (10, 10, (WIDTH-60)/5, MENU_HEIGHT-20))
        self.win.blit(self.font.render('Reset', True, BLACK), (40, 15))
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.win, LIGHT_GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE + MENU_HEIGHT, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == 0:
                    self.board[row].append(place_piece(row, col, 'black', self.win))
                    self.black_pieces.append(self.get_piece(row, col))
                elif row == 1:
                    self.board[row].append(Pawn(row, col, 'black', self.win, True))
                    self.black_pieces.append(self.get_piece(row, col))
                elif row == 6:
                    self.board[row].append(Pawn(row, col, 'white', self.win, True))
                    self.white_pieces.append(self.get_piece(row, col))
                elif row == 7:
                    self.board[row].append(place_piece(row, col, 'white', self.win))
                    self.white_pieces.append(self.get_piece(row, col))
                else:
                    self.board[row].append(0)
                
    
    def draw(self):
        self.draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]

                if piece != 0:
                    piece.draw(self.win)
    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if type(piece) == Pawn:
            piece.jump_two = False
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_valid_moves(self, piece):
        if piece != 0:
            moves = piece.valid_moves(self)
            return moves
        return set()
        

                

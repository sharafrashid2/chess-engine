import pygame
from .constants import SQUARE_SIZE, ROWS, COLS, MENU_HEIGHT
import sys, os

class Piece():
    def __init__(self, row, col, color, win):
        self.row = row
        self.col = col
        self.color = color
        self.win = win
        self.name = ""
        self.possible_moves = set()

        if self.color == 'white':
            self.direction = -1
        else:
            self.direction = 1
        
        self.x = 0
        self.y = 0
        self.calc_pos()
    
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + 5
        self.y = SQUARE_SIZE * self.row + 5 + MENU_HEIGHT
    
    def draw(self, win):
        if self.name != "":
            pawn_img = pygame.image.load(os.path.join('board_assets', f'{self.color}_{self.name}.png'))
            pawn_img = pygame.transform.scale(pawn_img, (SQUARE_SIZE-10, SQUARE_SIZE-10))
            win.blit(pawn_img, (self.x, self.y))
    
    def move(self, row, col):
        self.row, self.col = row, col
        self.calc_pos()
    
    def _traverse_straight(self, variable_start, variable_end, constant, direction, board, valid, label, threat_map = False):
        if direction == -1:
            interval = range(variable_start, -1, -1)
        else:
            interval = range(variable_start, variable_end)

        for variable in interval:
            if label == 'row':
                piece = board[variable][constant]
            else:
                piece = board[constant][variable]
            if variable != variable_start:
                if piece != 0 and piece.color == self.color:
                    if label == 'row' and threat_map:
                        valid.add((variable, constant))
                    elif threat_map:
                        valid.add((constant, variable))
                    break
                if label == 'row':
                    valid.add((variable, constant))
                else:
                    valid.add((constant, variable))
            if piece != 0 and variable != variable_start:
                break
    
    def _traverse_straight_all(self, board, valid, threat_map=False):
        if not threat_map:
            self._traverse_straight(self.row, ROWS, self.col, 1, board, valid, 'row')
            self._traverse_straight(self.row, ROWS, self.col, -1, board, valid, 'row')
            self._traverse_straight(self.col, COLS, self.row, 1, board, valid, 'col')
            self._traverse_straight(self.col, COLS, self.row, -1, board, valid, 'col')
        else:
            self._traverse_straight(self.row, ROWS, self.col, 1, board, valid, 'row', True)
            self._traverse_straight(self.row, ROWS, self.col, -1, board, valid, 'row', True)
            self._traverse_straight(self.col, COLS, self.row, 1, board, valid, 'col', True)
            self._traverse_straight(self.col, COLS, self.row, -1, board, valid, 'col', True)

        
    def _traverse_diagonal(self, board, row, col, direction, valid, threat_map=False):
        def condition_map(val1, val2, direction):
            if direction == 'right': 
                return val1 >= 0 and val2 < COLS
            if direction == 'right-opp': 
                return val1 < COLS and val2 >= 0
            if direction == 'left': 
                return val1 >= 0 and val2 >= 0
            if direction == 'left-opp': 
                return val1 < COLS and val2 < ROWS
        
        start = [row, col]
        current = start[:]
        if direction == 'right':
            condition = condition_map(current[0], current[1], 'right')
            incr_0, incr_1 = -1, 1
        elif direction == 'right-opp':
            condition = condition_map(current[0], current[1], 'right-opp')
            incr_0, incr_1 = 1, -1
        elif direction == 'left':
            condition = condition_map(current[0], current[1], 'left')
            incr_0, incr_1 = -1, -1
        elif direction == 'left-opp':
            condition = condition_map(current[0], current[1], 'left-opp')
            incr_0, incr_1 = 1, 1

        while condition:
            piece = board[current[0]][current[1]]
            if current != start:
                if piece != 0 and piece.color == self.color:
                    if threat_map:
                        valid.add(tuple(current))
                    break
                valid.add(tuple(current))
            if piece != 0 and current != start:
                break

            current[0] += incr_0
            current[1] += incr_1
            condition = condition_map(current[0], current[1], direction)
    
    def _traverse_diagonal_all(self, board, valid, threat_map=False):
        if not threat_map:
            self._traverse_diagonal(board, self.row, self.col, 'right', valid)
            self._traverse_diagonal(board, self.row, self.col, 'right-opp', valid)
            self._traverse_diagonal(board, self.row, self.col, 'left', valid)
            self._traverse_diagonal(board, self.row, self.col, 'left-opp', valid)
        else:
            self._traverse_diagonal(board, self.row, self.col, 'right', valid, True)
            self._traverse_diagonal(board, self.row, self.col, 'right-opp', valid, True)
            self._traverse_diagonal(board, self.row, self.col, 'left', valid, True)
            self._traverse_diagonal(board, self.row, self.col, 'left-opp', valid, True)
    
    def __repr__(self):
        return f"{self.color}_{self.name}"

      

class Pawn(Piece):
    def __init__(self, row, col, color, win, jump_two):
        Piece.__init__(self, row, col, color, win)
        self.jump_two = jump_two
        self.name = "pawn"

    def get_all_moves(self, board, used_jump_two_prev = False, threat_map = False):
        valid = set()
        if self.color == 'white':
            diagonal_check = [(self.row-1, self.col-1), (self.row-1, self.col+1)]
            direction = -1
        else:
            diagonal_check = [(self.row+1, self.col+1), (self.row+1, self.col-1)]
            direction = 1

        if (self.jump_two == True and board[self.row + direction][self.col] == 0 and 
            board[self.row + 2*direction][self.col] == 0 and not threat_map
        ):
            valid.add((self.row + 2*direction, self.col))

        if board[self.row + 1*direction][self.col] == 0 and not threat_map:
            valid.add((self.row + 1*direction, self.col))
        
        for coord in diagonal_check:
            if coord[0] in range(0, ROWS) and coord[1] in range(0, COLS):
                piece = board[coord[0]][coord[1]]
            else:
                continue
            if piece != 0 and piece.color != self.color and not threat_map:
                valid.add(coord)
            
            test = used_jump_two_prev

            if (piece == 0 and test and test[1] == 1 and abs(self.col - test[2].col) == 1 and
                self.row == test[2].row and abs(coord[0]-test[2].row) == 1 and coord[1] == test[2].col and
                not threat_map
            ):
                valid.add(coord)
            
            if threat_map:
                valid.add(coord)
        
        if not threat_map:
            self.possible_moves = valid

        return valid

    def get_threat_spots(self, board):
        return self.get_all_moves(board, threat_map=True)
        
class Bishop(Piece):
    def __init__(self, row, col, color, win):
        Piece.__init__(self, row, col, color, win)
        self.name = "bishop"
    
    def get_all_moves(self, board):
        valid = set()
        self._traverse_diagonal_all(board, valid)
        self.possible_moves = valid
        return valid
    
    def get_threat_spots(self, board):
        valid = set()
        self._traverse_diagonal_all(board, valid, True)
        return valid
    

class Knight(Piece):
    def __init__(self, row, col, color, win):
        Piece.__init__(self, row, col, color, win)
        self.name = "knight"

    def get_all_moves(self, board, threat_map = False):
        valid = set()
        to_check = [
                        (self.row - 2, self.col + 1), (self.row - 2, self.col - 1), (self.row + 2, self.col + 1), 
                        (self.row + 2, self.col - 1), (self.row + 1, self.col -2), (self.row + 1, self.col + 2),
                        (self.row - 1, self.col - 2), (self.row - 1, self.col + 2)
                   ]
        
        for coord in to_check:
            if coord[0] in range(0, ROWS) and coord[1] in range(0, COLS):
                piece = board[coord[0]][coord[1]]
            else:
                continue
            if piece == 0 or piece != 0 and piece.color != self.color:
                valid.add(coord)
            elif piece != 0 and piece.color == self.color and threat_map:
                valid.add(coord)

        if not threat_map:
            self.possible_moves = valid

        return valid
    
    def get_threat_spots(self, board):
        return self.get_all_moves(board, True)

class Rook(Piece):
    def __init__(self, row, col, color, win, moved):
        Piece.__init__(self, row, col, color, win)
        self.name = "rook"
        self.moved = moved
    
    def get_all_moves(self, board):
        valid = set()
        self._traverse_straight_all(board, valid)
        self.possible_moves = valid
        return valid
    
    def get_threat_spots(self, board):
        valid = set()
        self._traverse_straight_all(board, valid, True)
        return valid
        

class Queen(Piece):
    def __init__(self, row, col, color, win):
        Piece.__init__(self, row, col, color, win)
        self.name = "queen"
    
    def get_all_moves(self, board):
        valid = set()
        self._traverse_straight_all(board, valid)
        self._traverse_diagonal_all(board, valid)
        self.possible_moves = valid
        return valid
    
    def get_threat_spots(self, board):
        valid = set()
        self._traverse_straight_all(board, valid, True)
        self._traverse_diagonal_all(board, valid, True)
        return valid

class King(Piece):
    def __init__(self, row, col, color, win, moved):
        Piece.__init__(self, row, col, color, win)
        self.name = "king"
        self.moved = moved

    def get_all_moves(self, board, threat_map=False):
        valid = set()

        if self.moved == False:
            right_check = board[self.row][COLS-1]
            left_check = board[self.row][0]

            if (type(right_check) == Rook and right_check.moved == False and board[self.row][self.col+1] == 0 and
            board[self.row][self.col+2] == 0
            ):
                valid.add((self.row, self.col+2))
            
            if (type(left_check) == Rook and left_check.moved == False and board[self.row][self.col-1] == 0 and
            board[self.row][self.col-2] == 0 and board[self.row][self.col-3] == 0
            ):
                valid.add((self.row, self.col-2))
            
        for row in range(self.row-1, self.row+2):
            for col in range(self.col-1, self.col+2):
                if row in range(0, ROWS) and col in range(0, COLS) and (row, col) != (self.row, self.col):
                    piece = board[row][col]
                else:
                    continue
                if piece == 0 or (piece != 0 and piece.color != self.color):
                    valid.add((row, col))
                if threat_map:
                    valid.add((row, col))

        if not threat_map:
            self.possible_moves = valid
        
        return valid
    
    def get_threat_spots(self, board):
        return self.get_all_moves(board, True)
    
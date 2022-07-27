import pygame
import os
from chess.constants import SQUARE_SIZE, WIDTH, HEIGHT, MENU_HEIGHT
from chess.pieces import Rook, Queen, Bishop, Knight
from chess.board import Board
from chess.game import Game

FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def get_pos_from_mouse(pos):
    x, y = pos
    row = (y - MENU_HEIGHT) // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # reset button clicked
            pos = pygame.mouse.get_pos()
            if (event.type == pygame.MOUSEBUTTONDOWN and pos[0] >= 10 and pos[0] <= 10+(WIDTH-60)/5 and
                pos[1] >= 10 and pos[1] <= MENU_HEIGHT-20
                ):
                game.reset()
            # promotion to rook clicked
            elif game.promotion and (event.type == pygame.MOUSEBUTTONDOWN and pos[0] >= 20 + (WIDTH-60)/5 and 
                pos[0] <= 2*(10+(WIDTH-60)/5) and pos[1] >= 10 and pos[1] <= MENU_HEIGHT-20
                ):
                game.promote_pawn(Rook, *game.promote_unit)
                game.promotion = False
                game.promote_unit = None
                game.go_next_turn()

            # promotion to knight clicked
            elif game.promotion and (event.type == pygame.MOUSEBUTTONDOWN and pos[0] >= 30 + 2 * (WIDTH-60)/5 and 
                pos[0] <= 3*(10+(WIDTH-60)/5) and pos[1] >= 10 and pos[1] <= MENU_HEIGHT-20
                ):
                game.promote_pawn(Knight, *game.promote_unit)
                game.promotion = False
                game.promote_unit = None
                game.go_next_turn()

            # promotion to bishop clicked
            elif (game.promotion and event.type == pygame.MOUSEBUTTONDOWN and pos[0] >= 40 + 3 * (WIDTH-60)/5 and 
                pos[0] <= 4*(10+(WIDTH-60)/5) and pos[1] >= 10 and pos[1] <= MENU_HEIGHT-20
                ):
                game.promote_pawn(Bishop, *game.promote_unit)
                game.promotion = False
                game.promote_unit = None
                game.go_next_turn()

            # promotion to queen clicked
            elif game.promotion and (event.type == pygame.MOUSEBUTTONDOWN and pos[0] >= 50 + 4 * (WIDTH-60)/5 and 
                pos[0] <= 5*(10+(WIDTH-60)/5) and pos[1] >= 10 and pos[1] <= MENU_HEIGHT-20
                ):
                game.promote_pawn(Queen, *game.promote_unit)
                game.promotion = False
                game.promote_unit = None
                game.go_next_turn()

            # playing game as usual
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[1] > MENU_HEIGHT and game.promotion == False:
                row, col = get_pos_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()
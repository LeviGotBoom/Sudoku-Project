import pygame, sys
from sudoku_generator import *


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        pass
    #     Draws this cell, along with the value inside it.
	# If this cell has a nonzero value, that value is displayed.
	# Otherwise, no value is displayed in the cell.
	# The cell is outlined red if it is currently selected.


class Board:
    pass
#add functions

pygame.init()
PINK = (255, 237, 241)
FONT_COLOR = (0, 0, 0)
WIDTH = 600
HEIGHT = 650
START_FONT = pygame.font.Font(None, 60)

def main():
    screen = pygame.display.set_mode((600, 650))
    pygame.display.set_caption("Sudoku")


    screen.fill(PINK)

    start_text = "Welcome to Sudoku"
    end_surf = START_FONT.render(start_text, 0, FONT_COLOR)
    end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    screen.blit(end_surf, end_rect)

    pygame.display.update()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()




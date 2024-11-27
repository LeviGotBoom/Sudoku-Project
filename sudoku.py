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


PINK = (255, 182, 193)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 650))
    pygame.display.set_caption("Sudoku")


    screen.fill(PINK)
    pygame.display.update()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()




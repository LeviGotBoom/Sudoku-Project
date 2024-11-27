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
screen = pygame.display.set_mode((600, 650))

PINK = (255, 222, 222)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (196, 194, 194)
WIDTH = 600
HEIGHT = 650

START_FONT = pygame.font.Font(None, 60)
MED_FONT = pygame.font.Font(None, 45)
SMALL_FONT = pygame.font.Font(None, 25)


easy_button = pygame.Rect(100, 400, 100, 50)
medium_button = pygame.Rect(250, 400, 100, 50)
difficult_button = pygame.Rect(400, 400, 100, 50)



def main():

    pygame.display.set_caption("Sudoku")
    screen.fill(PINK)

    start_text = "Welcome to Sudoku"
    start_surf = START_FONT.render(start_text, 0, BLACK)
    start_rect = start_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    screen.blit(start_surf, start_rect)

    select_game = "Select Game Mode:"
    select_surf = MED_FONT.render(select_game, 0, BLACK)
    select_rect = select_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(select_surf, select_rect)


    pygame.display.update()

    def draw_button(button, text, color, hover_color):
        mouse_position = pygame.mouse.get_pos()

        if button.collidepoint(mouse_position):
            pygame.draw.rect(screen, hover_color, button)
        else:
            pygame.draw.rect(screen, color, button)

        text_surf = SMALL_FONT.render(text, 0, BLACK)
        rect_button = text_surf.get_rect(center=button.center)
        screen.blit(text_surf, rect_button)

        return button

    while True:

        draw_button(easy_button, "Easy", WHITE, DARK_GRAY)
        draw_button(medium_button, "Medium", WHITE, DARK_GRAY)
        draw_button(difficult_button, "Difficult", WHITE, DARK_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_button.collidepoint(event.pos):
                    pass
                    #implement easy mode board
                elif medium_button.collidepoint(event.pos):
                    pass
                    #implement medium mode board
                elif difficult_button.collidepoint(event.pos):
                    pass
                    #implement difficult mode board
        pygame.display.update()

if __name__ == '__main__':
    main()




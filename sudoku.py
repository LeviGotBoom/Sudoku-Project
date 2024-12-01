import pygame, sys
from sudoku_generator import *
import random

pygame.init()
screen = pygame.display.set_mode((600, 650))

PINK = (255, 222, 222)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (196, 194, 194)
WIDTH = 600
HEIGHT = 650

START_FONT = pygame.font.Font(None, 60)
MED_FONT = pygame.font.Font(None, 45)
SMALL_FONT = pygame.font.Font(None, 25)

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else "." for num in row))

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(self.row_length))

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num)
                and self.valid_in_col(col, num)
                and self.valid_in_box(row - row % 3, col - col % 3, num)
                )

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums.pop()

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self, row=0, col=0):
        if col == 9:
            row += 1
            col = 0

        if row == 9:
            return True

        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0

        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.sketched_value = 0

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        #Draw the cell and its content on the screen."""
        x, y = self.col * 60, self.row * 60
        cell_size = 60

        # Draw cell background
        pygame.draw.rect(self.screen, WHITE, (x, y, cell_size, cell_size))
        pygame.draw.rect(self.screen, BLACK, (x, y, cell_size, cell_size), 1)  # Cell border

        # Highlight if selected
        if self.selected:
            pygame.draw.rect(self.screen, RED, (x, y, cell_size, cell_size), 3)

        # Draw cell value or sketched value
        if self.value != 0:
            text = MED_FONT.render(str(self.value), True, BLACK)
            self.screen.blit(text, (x + 20, y + 15))  # Centered in the cell
        elif self.sketched_value != 0:
            text = SMALL_FONT.render(str(self.sketched_value), True, DARK_GRAY)
            self.screen.blit(text, (x + 5, y + 5))  # Top-left corner for sketched value

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, i, j, screen) for j in range(9)] for i in range(9)]
        self.selected_cell = None

    def draw(self):
        self.screen.fill(PINK)

        for row in self.cells:
            for cell in row:
                cell.draw()

        for i in range(10):
            line_width = 5 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, (0, i * 60), (540, i * 60), line_width)
            pygame.draw.line(self.screen, BLACK, (i * 60, 0), (i * 60, 540), line_width)

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if 0 <= x < 540 and 0 <= y < 540:
            row = y // 60
            col = x // 60
            return row, col
        return None

    def clear(self):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                if cell.value != 0:
                    cell.set_cell_value(0)
                    cell.set_sketched_value(0)

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def update_board(self):
        self.board = [[cell.value for cell in row] for row in self.cells]

    def find_empty(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell.value == 0:
                    return i, j
        return None

    def check_board(self):
        def valid_group(group):
            nums = [cell.value for cell in group if cell.value != 0]
            return len(nums) == len(set(nums))

        for i in range(9):
            if not valid_group(self.cells[i]) or not valid_group(self.cells[j][i] for j in range(9)):
                return False

        for box_row in range(3):
            for box_col in range(3):
                box = [self.cells[i][j]
                       for i in range(box_row * 3, box_row * 3 + 3)
                       for j in range(box_col * 3, box_col * 3 + 3)
                       ]
                if not valid_group(box):
                    return False

        return True


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

def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    generator.fill_values()
    generator.remove_cells()
    return generator.get_board()

def main():
    easy_button = pygame.Rect(100, 400, 100, 50)
    medium_button = pygame.Rect(250, 400, 100, 50)
    difficult_button = pygame.Rect(400, 400, 100, 50)

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

    difficulty = None

    while not difficulty:
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
                    difficulty = 30
                elif medium_button.collidepoint(event.pos):
                    difficulty = 40
                elif difficult_button.collidepoint(event.pos):
                    difficulty = 50

        pygame.display.update()

    board_data = generate_sudoku(9, difficulty)
    board = Board(WIDTH, HEIGHT - 50, screen, difficulty)

    for i in range(9):
        for j in range(9):
            board.cells[i][j].set_cell_value(board_data[i][j])

    reset_button = pygame.Rect(50, 560, 100, 40)
    restart_button = pygame.Rect(250, 560, 100, 40)
    exit_button = pygame.Rect(450, 560, 100, 40)

    running = True
    initial_board = [[cell.value for cell in row] for row in board.cells]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell = board.click(*pos)
                if cell:
                    board.select(*cell)
                elif reset_button.collidepoint(pos):
                    for i in range(9):
                        for j in range(9):
                            board.cells[i][j].set_cell_value(initial_board[i][j])
                            board.cells[i][j].set_sketched_value(0)
                elif restart_button.collidepoint(pos):
                    main()
                elif exit_button.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN:
                if board.selected_cell:
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        board.selected_cell.set_sketched_value(event.key - pygame.K_0)
                    elif event.key == pygame.K_RETURN:
                        if board.selected_cell.sketched_value:
                            board.selected_cell.set_cell_value(board.selected_cell.sketched_value)
                            board.selected_cell.set_sketched_value(0)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        board.selected_cell.set_cell_value(0)
                        board.selected_cell.set_sketched_value(0)
                    elif event.key == pygame.K_UP:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select(max(row - 1, 0), col)
                    elif event.key == pygame.K_DOWN:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select(min(row + 1, 8), col)
                    elif event.key == pygame.K_LEFT:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select(row, max(col - 1, 0))
                    elif event.key == pygame.K_RIGHT:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select(row, min(col + 1, 8))

        if board.is_full():
            if board.check_board():
                screen.fill(PINK)
                win_text = "Game Won!!"
                win_surf = START_FONT.render(win_text, 0, BLACK)
                win_rect = win_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(win_surf, win_rect)


                while True:
                    exit_button_win = pygame.Rect(250, HEIGHT // 2 + 50, 100, 40)
                    draw_button(exit_button_win, "EXIT", WHITE, DARK_GRAY)

                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if exit_button_win.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()

            else:
                screen.fill(PINK)
                lose_text = "Game Over :("
                lose_surf = START_FONT.render(lose_text, 0, BLACK)
                lose_rect = lose_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(lose_surf, lose_rect)

                restart_button_lose = pygame.Rect(150, HEIGHT // 2 + 50, 100, 40)
                exit_button_lose = pygame.Rect(350, HEIGHT // 2 + 50, 100, 40)


                while True:
                    restart_button_lose = pygame.Rect(150, HEIGHT // 2 + 50, 100, 40)
                    exit_button_lose = pygame.Rect(350, HEIGHT // 2 + 50, 100, 40)
                    draw_button(restart_button_lose, "RESTART", WHITE, DARK_GRAY)
                    draw_button(exit_button_lose, "EXIT", WHITE, DARK_GRAY)

                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if restart_button_lose.collidepoint(event.pos):
                                main()
                            elif exit_button_lose.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()

        board.update_board()
        board.draw()

        draw_button(reset_button, "RESET", WHITE, DARK_GRAY)
        draw_button(restart_button, "RESTART", WHITE, DARK_GRAY)
        draw_button(exit_button, "EXIT", WHITE, DARK_GRAY)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
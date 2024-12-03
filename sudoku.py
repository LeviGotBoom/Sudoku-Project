import pygame, sys
from sudoku_generator import *
import random
import time

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

        import os
        terminal_width = os.get_terminal_size().columns
        board_width = self.row_length * 4

        padding = max((terminal_width - board_width) // 2, 0)

        for row in self.board:
            formatted_row = " | ".join(str(cell) if cell != 0 else " " for cell in row)
            print(" " * padding + "| " + formatted_row + " |")

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
        self.immutable = value != 0

    def set_cell_value(self, value):
        if not self.immutable:
            self.value = value

    def set_sketched_value(self, value):
        if not self.immutable:
            self.sketched_value = value

    def draw(self, offset_x=0, offset_y=0):
        # Draw the cell and its content on the screen
        x, y = self.col * 60 + offset_x, self.row * 60 + offset_y
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
            text_rect = text.get_rect(center=(x + cell_size / 2, y + cell_size / 2))  # Centered text
            self.screen.blit(text, text_rect)

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
        self.offset_x = (WIDTH - 540) // 2 # centers it horizontally
        self.offset_y = (HEIGHT - 540) // 2 - 20  # offcentered to make space for buttons

    def draw(self):
        self.screen.fill(PINK)

        for row in self.cells:
            for cell in row:
                cell.draw(self.offset_x, self.offset_y)

        for i in range(10):
            line_width = 5 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK,
                             (self.offset_x, self.offset_y + i * 60),
                             (self.offset_x + 540, self.offset_y + i * 60), line_width)
            pygame.draw.line(self.screen, BLACK,
                             (self.offset_x + i * 60, self.offset_y),
                             (self.offset_x + i * 60, self.offset_y + 540), line_width)
    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if self.offset_x <= x < self.offset_x + 540 and self.offset_y <= y < self.offset_y + 540:
            row = (y - self.offset_y) // 60
            col = (x - self.offset_x) // 60
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

def select_mode(subtitle, button_names, options):
    button_one = pygame.Rect(100, 400, 100, 50)
    button_two = pygame.Rect(250, 400, 100, 50)
    button_three = pygame.Rect(400, 400, 100, 50)
    mode_value = None

    screen.fill(PINK)

    #
    # arrow_image = pygame.image.load("pinkarrowkeys.png")
    # arrow_image = pygame.transform.scale(arrow_image, (50, 50))
    #
    # screen.blit(arrow_image, (WIDTH // 2 - arrow_image.get_width() // 2, HEIGHT // 2 - 200))

    start_text = "Welcome to Sudoku"
    start_surf = START_FONT.render(start_text, 0, BLACK)
    start_rect = start_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    screen.blit(start_surf, start_rect)

    select_surf = MED_FONT.render(subtitle, 0, BLACK)
    select_rect = select_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(select_surf, select_rect)
    pygame.display.update()



    while not mode_value:
        draw_button(button_one, button_names[0], WHITE, DARK_GRAY)
        draw_button(button_two, button_names[1], WHITE, DARK_GRAY)
        draw_button(button_three, button_names[2], WHITE, DARK_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_one.collidepoint(event.pos):
                    mode_value = options[0]
                elif button_two.collidepoint(event.pos):
                    mode_value = options[1]
                elif button_three.collidepoint(event.pos):
                    mode_value = options[2]

        pygame.display.update()
    return mode_value

def game_over():
    lose_surf = START_FONT.render("Game Over :(", 0, BLACK)
    lose_rect = lose_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(lose_surf, lose_rect)

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

def main():

    pygame.display.set_caption("Sudoku")

    difficulty = select_mode("Select Game Mode:", ["Easy", "Medium", "Difficult"], [30, 40, 50])
    time_mode = select_mode("Select Time Mode:", ["Unlimited", "3 Min", "5 Min"], [-1, 3, 5])

    start_ticks = pygame.time.get_ticks()

    board_data = generate_sudoku(9, difficulty)
    board = Board(WIDTH, HEIGHT - 50, screen, difficulty)

    for i in range(9):
        for j in range(9):
            board.cells[i][j].set_cell_value(board_data[i][j])
            board.cells[i][j].immutable = board_data[i][j] != 0

    reset_button = pygame.Rect(50, 590, 100, 40)
    restart_button = pygame.Rect(250, 590, 100, 40)
    exit_button = pygame.Rect(450, 590, 100, 40) #moves buttons

    win_image = pygame.image.load("cartoon_crown.png")
    win_image = pygame.transform.scale(win_image, (150, 150))


    running = True
    initial_board = [[cell.value for cell in row] for row in board.cells]

    while running:
        #time information
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Time in seconds
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"Time: {minutes:02}:{seconds:02}"

        if time_mode != -1:
            timer_text += f" / {time_mode:02}:00"

        if minutes >= time_mode != -1:
            message = f"Your {time_mode} minutes are up."
            screen.fill(PINK)
            lose_surf = START_FONT.render(message, 0, BLACK)
            lose_rect = lose_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
            screen.blit(lose_surf, lose_rect)

            game_over()

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
                    start_ticks = pygame.time.get_ticks()
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

                screen.blit(win_image, (WIDTH // 2 - win_image.get_width() // 2, HEIGHT // 2 - 100 - 60))

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
                game_over()

        board.update_board()
        board.draw()

        # creating the timer
        font_timer = pygame.font.Font(None, 35)
        timer_surface = font_timer.render(timer_text, True, BLACK)
        timer_rect = timer_surface.get_rect(center=(WIDTH // 2, 20))
        screen.blit(timer_surface, timer_rect)

        draw_button(reset_button, "RESET", WHITE, DARK_GRAY)
        draw_button(restart_button, "RESTART", WHITE, DARK_GRAY)
        draw_button(exit_button, "EXIT", WHITE, DARK_GRAY)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

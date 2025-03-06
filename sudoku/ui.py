import pygame
import sys
import os
from button_for_ui import Button
#from board_util import extract_board

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (50, 50, 255)
CELL_SIZE = 60
GRID_SIZE = 9

pygame.init()
pygame.font.init()

  # Để đảm bảo board luôn là 2D list
def extract_board(obj):
    """
    Nếu obj có thuộc tính 'state', trả về obj.state, ngược lại trả về obj.
    """
    if hasattr(obj, "state"):
        return obj.state
    return obj


class SudokuUI:
    def __init__(self, puzzle):
        """
        puzzle: Đối tượng SudoPuzzle đã giải, có thuộc tính solution_path chứa danh sách các state (2D list).
        """
        self.puzzle = puzzle
        if hasattr(puzzle, 'solution_path') and puzzle.solution_path:
            self.solution_path = puzzle.solution_path
        else:
            self.solution_path = [puzzle.board]
        self.step_index = 0

        self.board = self.solution_path[self.step_index]
        # Lấy board dưới dạng 2D list bằng extract_board
        self.board = extract_board(self.solution_path[self.step_index])
        self.selected = None
        self.font = pygame.font.SysFont("comicsans", 40)

        self.WIDTH, self.HEIGHT = 1000, 700
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku - Step by Step")

        next_img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'next.png'))
        self.next_button = Button(800, 100, next_img, 0.8)

        pre_img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'previous.png'))
        self.pre_button = Button(650, 100, pre_img, 0.8)

        auto_img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'autorun.png'))
        self.auto_button = Button(700, 200, auto_img, 0.5)

        self.auto_mode = False

    def next_step(self):
        if self.step_index >= len(self.solution_path) - 1:
            return False
        self.step_index += 1
        self.board = extract_board(self.solution_path[self.step_index])
        return True

    def previous_step(self):
        if self.step_index <= 0:
            return False
        self.step_index -= 1
        self.board = extract_board(self.solution_path[self.step_index])
        return True


    def auto_run_next(self):
        """Tự động chạy các bước tiếp theo"""
        while self.next_step():
            # Xử lý các sự kiện để cửa sổ luôn phản hồi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.display()
            pygame.display.update()
            pygame.time.delay(200)

    def auto_run_previous(self):
        """Tự động chạy các bước ngược lại"""
        while self.previous_step():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.display()
            pygame.display.update()
            pygame.time.delay(200)


    def draw_grid(self):
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.win, BLACK, (0, i * CELL_SIZE), (CELL_SIZE * GRID_SIZE, i * CELL_SIZE), thickness)
            pygame.draw.line(self.win, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, CELL_SIZE * GRID_SIZE), thickness)

    def draw_numbers(self):
        board = extract_board(self.board)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                val = board[i][j]
                if val is None:
                    val = 0
                if val != 0:
                    text = self.font.render(str(val), True, BLACK)
                    x = j * CELL_SIZE + (CELL_SIZE - text.get_width()) // 2
                    y = i * CELL_SIZE + (CELL_SIZE - text.get_height()) // 2
                    self.win.blit(text, (x, y))

    def highlight_cell(self):
        if self.selected is not None:
            row, col = self.selected
            pygame.draw.rect(self.win, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

    def display(self):
        self.win.fill(WHITE)
        self.draw_numbers()
        self.draw_grid()
        self.highlight_cell()

    def click(self, pos):
        if pos[0] < CELL_SIZE * GRID_SIZE and pos[1] < CELL_SIZE * GRID_SIZE:
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            self.selected = (row, col)

    def place_number(self, value):
        if self.selected is not None:
            row, col = self.selected
            self.board[row][col] = value

    def running(self):
        clock = pygame.time.Clock()
        # Hiển thị
        self.display()
        pygame.display.update()
        print("Displaying initial puzzle.")
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # chỉ set running = False, không gọi sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < CELL_SIZE * GRID_SIZE and pos[1] < CELL_SIZE * GRID_SIZE:
                        self.click(pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.next_step()
                    if event.key == pygame.K_p:
                        self.previous_step()
                    if event.unicode in "0123456789":
                        try:
                            num = int(event.unicode)
                        except:
                            num = 0
                        self.place_number(num)
            self.display()
            # Xử lý nút Next
            if self.next_button.draw(self.win):
                if self.auto_mode:
                    self.auto_run_next()
                else:
                    self.next_step()
                    pygame.time.delay(300)
            # Xử lý nút Previous
            if self.pre_button.draw(self.win):
                if self.auto_mode:
                    self.auto_run_previous()
                else:
                    self.previous_step()
                    pygame.time.delay(300)
            # Xử lý nút Auto-run: bật/tắt chế độ tự động
            if self.auto_button.draw(self.win):
                self.auto_mode = not self.auto_mode
                pygame.time.delay(300)

            # Vẽ thông báo nếu auto_mode đang bật
            if self.auto_mode:
                font = pygame.font.SysFont("comicsans", 20)
                text_surface = font.render("Auto-run is turned on", True, (0, 0, 0))  # màu đen
                # Tùy chỉnh vị trí hiển thị (x, y) cho phù hợp
                self.win.blit(text_surface, (700, 270))

            pygame.display.update()
        pygame.quit()


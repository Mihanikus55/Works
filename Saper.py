import sys

from random import randrange
import pygame
from pygame.locals import *


class Board:
    def __init__(self, width, height, left, top, cell_size):
        self.width = width
        self.height = height
        self.set_view(left, top, cell_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top + 30
        self.cell_size = cell_size

    def generate_board(self):
        self.board = [[-1] * self.width for _ in range(self.height)]

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos

        col = (x - self.left) // self.cell_size
        row = (y - self.top) // self.cell_size
        if 0 <= col < self.width and 0 <= row < self.height:
            return row, col

        return None

    def on_click(self, cell):
        if cell is None:
            return

        row, col = cell

        value = self.board[row][col]
        if value == -1:
            mine.open_cell(row, col)
        return


class Minesweeper(Board):
    def __init__(self, width, height, mines_n, left=10, top=10, cell_size=30):
        super().__init__(width, height, left, top, cell_size)
        self.mines_n = mines_n
        self.font = pygame.font.Font(None, self.cell_size - 20)
        self.to_deault()

    def to_deault(self):
        self.generate_board()
        self.generate_mines()
        self.opened_cells = 0

    def top_menu_draw_text(self, screen):
        text1 = self.font.render(f"Mines: {self.mines_n}", True, (100, 255, 100))
        screen.blit(text1, (self.left, self.left))

        text2 = self.font.render(f"Opened cells: {self.opened_cells}", True, (100, 255, 100))
        screen.blit(text2, (self.left * 3 + text1.get_width(), self.left))

    def generate_mines(self):
        n = self.mines_n
        while n > 0:
            row = randrange(0, self.height)
            col = randrange(0, self.width)
            if self.board[row][col] != 10:
                self.board[row][col] = 10
                n -= 1

    def open_cell(self, row, col):
        if self.board[row][col] != -1:
            return
        mines = 0
        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                r_index = row + i
                c_index = col + j

                if (0 <= r_index < self.height and 0 <= c_index < self.width and
                        self.board[r_index][c_index] == 10):
                    mines += 1
                elif (0 <= r_index < self.height and 0 <= c_index < self.width and
                        self.board[r_index][c_index] == -1):
                    cells.append((r_index, c_index))

        self.board[row][col] += mines + 1
        self.opened_cells += 1

        if not mines:
            for cell in cells:
                self.open_cell(*cell)

    def draw_num(self, x, y, value):
        num = self.font.render(str(value), True, (100, 255, 100))
        screen.blit(num, (x + self.cell_size // 10, y + self.cell_size // 10))

    def render(self, screen):
        self.top_menu_draw_text(screen)

        for row_index in range(self.height):
            for col_index in range(self.width):
                x = col_index * self.cell_size + self.left
                y = row_index * self.cell_size + self.top
                value = self.board[row_index][col_index]
                if value == 10:
                    pygame.draw.rect(screen, 'red', (x, y, self.cell_size, self.cell_size))
                elif value >= 0:
                    self.draw_num(x, y, value)
                pygame.draw.rect(screen, 'grey50', (x, y, self.cell_size, self.cell_size), 1)


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

c_w = 10
c_h = 15

c_s = 50

m_n = 10

l_t = 10

width, height = c_w * c_s + l_t * 2, c_h * c_s + l_t * 2 + 30  # 30 - отступ под шапку
screen = pygame.display.set_mode((width, height))

mine = Minesweeper(c_w, c_h, m_n, left=l_t, top=l_t, cell_size=c_s)

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mine.get_click(event.pos)

        if event.type == KEYDOWN:
            if event.key == K_c:
                mine.to_deault()

    mine.render(screen)

    pygame.display.flip()
    fpsClock.tick(fps)

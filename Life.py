import sys

from copy import deepcopy
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
        self.board = [[0] * self.width for _ in range(self.height)]

    def top_menu_draw_text(self, screen):
        font = pygame.font.Font(None, 23)

        text1 = font.render(f"Speed: {life.frame_life_speed}", True, (100, 255, 100))
        screen.blit(text1, (self.left, self.left))

        text2 = font.render(f"Running: {life.is_running}", True, (100, 255, 100))
        screen.blit(text2, (self.left * 3 + text1.get_width(), self.left))

    def render(self, screen):
        self.top_menu_draw_text(screen)

        for row_index in range(self.height):
            for col_index in range(self.width):
                x = col_index * self.cell_size + self.left
                y = row_index * self.cell_size + self.top
                value = self.board[row_index][col_index]
                if value:
                    pygame.draw.rect(screen, 'green', (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, 'grey50', (x, y, self.cell_size, self.cell_size), 1)

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
        self.board[row][col] = 1 if value == 0 else 0


class Life(Board):
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        super().__init__(width, height, left, top, cell_size)
        self.to_deault()

    def to_deault(self):
        self.generate_board()
        self.is_running = False
        self.frame_life_speed = 3

    def toggle_state(self):
        self.is_running = not self.is_running

    def change_speed(self, wheel_event):

        if 0.5 < self.frame_life_speed + wheel_event < fps:
            self.frame_life_speed += wheel_event * 0.5

    def next_move(self):
        if not self.is_running:
            return

        new_board = []

        for row_index, row in enumerate(self.board):
            new_row = []
            for col_index, cell in enumerate(row):
                neighbours = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == j == 0:
                            continue
                        r_index = (row_index + i) % self.height
                        c_index = (col_index + j) % self.width
                        if (0 <= r_index < self.height and 0 <= c_index < self.width and
                                self.board[r_index][c_index]):
                            neighbours += 1

                if neighbours > 3 or neighbours < 2:
                    new_row.append(0)
                elif neighbours == 3:
                    new_row.append(1)
                else:
                    new_row.append(self.board[row_index][col_index])

            new_board.append(new_row)
        self.board = deepcopy(new_board)

        fpsClock.tick(self.frame_life_speed)


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

c_w = 40
c_h = 30
c_s = 15

l_t = 10

width, height = c_w * c_s + l_t * 2, c_h * c_s + l_t * 2 + 30  # 30 - отступ под шапку
screen = pygame.display.set_mode((width, height))

life = Life(c_w, c_h, left=l_t, top=l_t, cell_size=c_s)

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if not life.is_running and event.button == 1:
                life.get_click(event.pos)
            if event.button == 3:
                life.toggle_state()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                life.toggle_state()
            if event.key == K_c:
                life.to_deault()

        if event.type == MOUSEWHEEL:
            life.change_speed(event.y)

    life.next_move()

    life.render(screen)

    pygame.display.flip()
    fpsClock.tick(fps)

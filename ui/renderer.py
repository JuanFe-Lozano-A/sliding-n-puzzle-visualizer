import pygame
import time
from ui.colors import *

class Renderer:
    def __init__(self, screen, board, cell_size=80):
        self.screen = screen
        self.board = board
        self.cell_size = cell_size
        self.font = pygame.font.Font(None, 50)

    def draw_grid(self):
        for i in range(self.board.n + 1):
            pygame.draw.line(self.screen, BLACK, (0, i * self.cell_size), (self.board.n * self.cell_size, i * self.cell_size))
            pygame.draw.line(self.screen, BLACK, (i * self.cell_size, 0), (i * self.cell_size, self.board.n * self.cell_size))

    def draw_pieces(self):
        for i in range(self.board.n):
            for j in range(self.board.n):
                if self.board.grid[i][j] != 0:
                    text = self.font.render(str(self.board.grid[i][j]), True, BLACK)
                    text_rect = text.get_rect(center=(j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

    def highlight_piece(self, piece_pos, color=GREEN, duration=0.2):
        i, j = piece_pos
        rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect, 5)
        pygame.display.flip()
        time.sleep(duration)

    def move_animation(self, from_pos, to_pos, duration=0.5):
        start_time = time.time()
        from_i, from_j = from_pos
        to_i, to_j = to_pos
        val = self.board.grid[to_i][to_j] # The value is already swapped in the board logic

        while time.time() - start_time < duration:
            progress = (time.time() - start_time) / duration
            curr_i = from_i + (to_i - from_i) * progress
            curr_j = from_j + (to_j - from_j) * progress

            # Clear the area
            self.screen.fill(WHITE)
            self.draw_grid()
            # Redraw all pieces except the moving one
            for r in range(self.board.n):
                for c in range(self.board.n):
                    if (r,c) != from_pos and (r,c) != to_pos:
                         if self.board.grid[r][c] != 0:
                            text = self.font.render(str(self.board.grid[r][c]), True, BLACK)
                            text_rect = text.get_rect(center=(c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2))
                            self.screen.blit(text, text_rect)


            # Draw the moving piece
            text = self.font.render(str(val), True, BLACK)
            text_rect = text.get_rect(center=(curr_j * self.cell_size + self.cell_size // 2, curr_i * self.cell_size + self.cell_size // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()

    def render(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_pieces()
        pygame.display.flip()

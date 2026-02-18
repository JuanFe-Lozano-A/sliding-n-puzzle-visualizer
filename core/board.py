import numpy as np

class Board:
    def __init__(self, n):
        self.n = n
        self.grid = np.arange(1, n*n + 1).reshape((n, n))
        self.empty_pos = (n-1, n-1)
        self.grid[self.empty_pos] = 0  # 0 represents the empty space

    def get_grid(self):
        return self.grid

    def get_empty_pos(self):
        return self.empty_pos

    def move(self, direction):
        y, x = self.empty_pos
        if direction == "UP":
            if y > 0:
                self.grid[y][x], self.grid[y-1][x] = self.grid[y-1][x], self.grid[y][x]
                self.empty_pos = (y-1, x)
                return True
        elif direction == "DOWN":
            if y < self.n - 1:
                self.grid[y][x], self.grid[y+1][x] = self.grid[y+1][x], self.grid[y][x]
                self.empty_pos = (y+1, x)
                return True
        elif direction == "LEFT":
            if x > 0:
                self.grid[y][x], self.grid[y][x-1] = self.grid[y][x-1], self.grid[y][x]
                self.empty_pos = (y, x-1)
                return True
        elif direction == "RIGHT":
            if x < self.n - 1:
                self.grid[y][x], self.grid[y][x+1] = self.grid[y][x+1], self.grid[y][x]
                self.empty_pos = (y, x+1)
                return True
        return False

    def is_solved(self):
        return np.array_equal(self.grid, np.arange(1, self.n*self.n + 1).reshape((self.n, self.n)))

    def __str__(self):
        return str(self.grid)

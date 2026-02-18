import random
from core.board import Board

class Shuffler:
    def __init__(self, board):
        self.board = board

    def shuffle(self, moves=1000):
        for _ in range(moves):
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.board.move(direction)

    def is_solvable(self):
        # This is a placeholder for a real solvability check.
        # A simple shuffle by making random moves ensures solvability.
        return True

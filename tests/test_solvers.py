import unittest
import numpy as np
from core.board import Board
from solvers.a_star import AStarSolver
from solvers.bfs import BFSSolver

class TestSolvers(unittest.TestCase):
    def test_a_star_solver(self):
        board = Board(2)
        board.grid = np.array([[1, 2], [3, 0]])
        solver = AStarSolver(board)
        solution = solver.solve()
        self.assertIsNotNone(solution)
        self.assertIsInstance(solution, list)

    def test_bfs_solver(self):
        board = Board(2)
        board.grid = np.array([[1, 2], [3, 0]])
        solver = BFSSolver(board)
        solution = solver.solve()
        self.assertIsNotNone(solution)
        self.assertIsInstance(solution, list)

if __name__ == '__main__':
    unittest.main()

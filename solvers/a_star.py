import numpy as np
import heapq
from solvers.base_solver import BaseSolver
from solvers.heuristics import manhattan_distance

class AStarSolver(BaseSolver):
    def __init__(self, board, heuristic=manhattan_distance):
        super().__init__(board)
        self.heuristic = heuristic

    def solve(self):
        # The priority queue will store tuples of (cost, path, board_state)
        frontier = [(self.heuristic(self.board), [], self.board)]
        explored = set()

        while frontier:
            cost, path, current_board = heapq.heappop(frontier)

            if current_board.is_solved():
                return path

            state_tuple = tuple(map(tuple, current_board.get_grid()))
            if state_tuple in explored:
                continue

            explored.add(state_tuple)

            for move in ["UP", "DOWN", "LEFT", "RIGHT"]:
                new_board = current_board.__class__(current_board.n)
                new_board.grid = np.copy(current_board.get_grid())
                new_board.empty_pos = current_board.get_empty_pos()


                if new_board.move(move):
                    new_path = path + [move]
                    new_cost = len(new_path) + self.heuristic(new_board)
                    heapq.heappush(frontier, (new_cost, new_path, new_board))

        return None  # No solution found

    def get_decision_basis(self):
        return "Choosing the move that minimizes the cost (g) + heuristic (h)."

    def get_metrics(self):
        return {"Manhattan Distance": self.heuristic(self.board)}

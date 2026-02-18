from solvers.base_solver import BaseSolver
from collections import deque

class BFSSolver(BaseSolver):
    def __init__(self, board):
        super().__init__(board)

    def solve(self):
        queue = deque([(self.board.get_grid().tobytes(), [])])
        visited = {self.board.get_grid().tobytes()}

        while queue:
            current_grid_bytes, path = queue.popleft()
            current_grid = np.frombuffer(current_grid_bytes, dtype=int).reshape(self.board.n, self.board.n)

            if np.array_equal(current_grid, np.arange(1, self.board.n*self.board.n + 1).reshape((self.board.n, self.board.n))):
                return path

            empty_pos = tuple(np.argwhere(current_grid == 0)[0])

            for move in ["UP", "DOWN", "LEFT", "RIGHT"]:
                new_board = self.board.__class__(self.board.n)
                new_board.grid = np.copy(current_grid)
                new_board.empty_pos = empty_pos

                if new_board.move(move):
                    new_grid_bytes = new_board.get_grid().tobytes()
                    if new_grid_bytes not in visited:
                        visited.add(new_grid_bytes)
                        new_path = path + [move]
                        queue.append((new_grid_bytes, new_path))
        return None

    def get_decision_basis(self):
        return "Exploring all possible moves at the current depth."

    def get_metrics(self):
        return {}

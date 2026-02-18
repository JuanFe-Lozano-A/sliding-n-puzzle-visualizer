import numpy as np
from collections import deque
from solvers.base_solver import BaseSolver

class BFSSolver(BaseSolver):
    def __init__(self, board):
        super().__init__(board)
        self.nodes_explored = 0
        self.path_cost = 0
        
        # Pre-calculate goal state once
        n = board.n
        self.goal_state = tuple(list(range(1, n*n)) + [0])

    def solve(self):
        """
        BFS using state tuples and parent pointers for efficiency.
        - Uses flat tuple states instead of 2D grids
        - Uses parent pointers instead of storing full paths
        - Reduces memory significantly
        """
        n = self.board.n
        start_state = tuple(self.board.grid.flatten())
        
        if start_state == self.goal_state:
            return []
        
        # Queue stores only states (not full paths)
        queue = deque([start_state])
        visited = {start_state}
        parent_map = {}  # state -> (parent_state, move_taken)
        
        while queue:
            current_state = queue.popleft()
            self.nodes_explored += 1
            
            if current_state == self.goal_state:
                # Reconstruct path from parent pointers
                self.path_cost = self._get_depth(parent_map, current_state)
                return self._reconstruct_path(parent_map, current_state)
            
            # Convert state tuple to grid for easier manipulation
            current_grid = np.array(current_state, dtype=int).reshape(n, n)
            empty_pos = tuple(np.argwhere(current_grid == 0)[0])
            y, x = empty_pos
            
            # Try all 4 moves
            moves = [
                ("UP", -1, 0),
                ("DOWN", 1, 0),
                ("LEFT", 0, -1),
                ("RIGHT", 0, 1)
            ]
            
            for move_name, dy, dx in moves:
                ny, nx = y + dy, x + dx
                
                if 0 <= ny < n and 0 <= nx < n:
                    # Create new state by swapping
                    new_grid = current_grid.copy()
                    new_grid[y, x], new_grid[ny, nx] = new_grid[ny, nx], new_grid[y, x]
                    new_state = tuple(new_grid.flatten())
                    
                    if new_state not in visited:
                        visited.add(new_state)
                        parent_map[new_state] = (current_state, move_name)
                        queue.append(new_state)
        
        return None  # No solution found

    def _reconstruct_path(self, parent_map, goal_state):
        """Reconstruct path from parent pointers - O(depth) operation"""
        path = []
        current_state = goal_state
        
        while current_state in parent_map:
            parent_state, move = parent_map[current_state]
            path.append(move)
            current_state = parent_state
        
        return list(reversed(path))
    
    def _get_depth(self, parent_map, state):
        """Calculate depth by counting parent chain"""
        depth = 0
        current = state
        while current in parent_map:
            depth += 1
            current = parent_map[current][0]
        return depth

    def get_decision_basis(self):
        return "Exploring all nodes at depth d before exploring depth d+1"

    def get_metrics(self):
        return {
            "Nodes Explored": self.nodes_explored,
            "Path Cost": self.path_cost,
            "Algorithm": "BFS"
        }


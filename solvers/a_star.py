import heapq
import numpy as np
from solvers.base_solver import BaseSolver
from solvers.heuristics import manhattan_distance_incremental, manhattan_distance

class AStarSolver(BaseSolver):
    def __init__(self, board, heuristic=manhattan_distance):
        super().__init__(board)
        self.heuristic = heuristic
        self.nodes_explored = 0
        self.path_cost = 0
        
        # Pre-calculate goal state once
        n = board.n
        self.goal_state = tuple(list(range(1, n*n)) + [0])

    def solve(self):
        """
        A* search using state tuples and parent pointers for efficiency.
        - Stores only state hashes, not full Board objects
        - Uses parent pointers to reconstruct path (O(depth) instead of O(nodes))
        - Reduces memory from O(nodes * depth) to O(nodes)
        """
        n = self.board.n
        start_state = tuple(self.board.grid.flatten())
        
        if start_state == self.goal_state:
            return []
        
        # Priority queue: (cost, depth, state)
        frontier = [(self.heuristic(self.board), 0, start_state)]
        
        # Track visited states and their parents for path reconstruction
        visited = set()
        parent_map = {}  # state -> (parent_state, move_taken)
        cost_map = {start_state: 0}  # state -> g(n)
        
        while frontier:
            _, depth, current_state = heapq.heappop(frontier)
            
            if current_state in visited:
                continue
                
            visited.add(current_state)
            self.nodes_explored += 1
            
            if current_state == self.goal_state:
                # Reconstruct path from parent pointers
                self.path_cost = depth
                return self._reconstruct_path(parent_map, current_state)
            
            # Find empty position in current state
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
                        new_g = cost_map[current_state] + 1
                        
                        if new_state not in cost_map or new_g < cost_map[new_state]:
                            cost_map[new_state] = new_g
                            
                            # Calculate heuristic for new state
                            temp_board = self.board.__class__(n)
                            temp_board.grid = new_grid
                            new_h = self.heuristic(temp_board)
                            new_f = new_g + new_h
                            
                            # Store parent info for path reconstruction
                            parent_map[new_state] = (current_state, move_name)
                            
                            heapq.heappush(frontier, (new_f, new_g, new_state))
        
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

    def get_decision_basis(self):
        return "Choosing move that minimizes f(n) = g(n) + h(n)"

    def get_metrics(self):
        return {
            "Nodes Explored": self.nodes_explored,
            "Path Cost": self.path_cost,
            "Algorithm": "A*"
        }


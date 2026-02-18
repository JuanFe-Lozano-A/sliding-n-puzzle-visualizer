import numpy as np

def manhattan_distance(board):
    """
    Calculate Manhattan distance heuristic.
    Sum of distances from each tile to its goal position.
    """
    distance = 0
    n = board.n
    for i in range(n):
        for j in range(n):
            value = board.grid[i][j]
            if value != 0:
                target_x = (value - 1) % n
                target_y = (value - 1) // n
                distance += abs(i - target_y) + abs(j - target_x)
    return distance

def manhattan_distance_incremental(grid, old_grid, moved_value, old_pos, new_pos, n):
    """
    Incrementally update Manhattan distance when a tile moves.
    O(1) operation instead of O(n²).
    
    Args:
        grid: Current grid state
        old_grid: Previous grid state
        moved_value: Value of tile that moved
        old_pos: Previous position of moved tile
        new_pos: New position of moved tile
        n: Board dimension
    
    Returns:
        Change in Manhattan distance (positive means increase, negative means decrease)
    """
    if moved_value == 0:  # Empty space doesn't count
        return 0
    
    target_x = (moved_value - 1) % n
    target_y = (moved_value - 1) // n
    
    old_distance = abs(old_pos[0] - target_y) + abs(old_pos[1] - target_x)
    new_distance = abs(new_pos[0] - target_y) + abs(new_pos[1] - target_x)
    
    return new_distance - old_distance

def hamming_distance(board):
    """
    Hamming distance heuristic.
    Number of tiles in wrong position (less accurate than Manhattan).
    """
    distance = 0
    n = board.n
    for i in range(n):
        for j in range(n):
            if board.grid[i][j] != 0 and board.grid[i][j] != i * n + j + 1:
                distance += 1
    return distance

def linear_conflict(board):
    """
    Linear conflict heuristic.
    More accurate than Manhattan distance but O(n²) to calculate.
    Useful for smaller boards (4x4 and below).
    """
    distance = manhattan_distance(board)
    n = board.n
    
    # Count conflicts in rows
    for i in range(n):
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                val1 = board.grid[i][j1]
                val2 = board.grid[i][j2]
                
                if val1 != 0 and val2 != 0:
                    target_row1 = (val1 - 1) // n
                    target_row2 = (val2 - 1) // n
                    
                    if (target_row1 == i and target_row2 == i and 
                        (val1 - 1) % n > (val2 - 1) % n):
                        distance += 2
    
    # Count conflicts in columns
    for j in range(n):
        for i1 in range(n):
            for i2 in range(i1 + 1, n):
                val1 = board.grid[i1][j]
                val2 = board.grid[i2][j]
                
                if val1 != 0 and val2 != 0:
                    target_col1 = (val1 - 1) % n
                    target_col2 = (val2 - 1) % n
                    
                    if (target_col1 == j and target_col2 == j and 
                        (val1 - 1) // n > (val2 - 1) // n):
                        distance += 2
    
    return distance

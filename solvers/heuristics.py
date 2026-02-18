import numpy as np

def manhattan_distance(board):
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

def hamming_distance(board):
    distance = 0
    n = board.n
    for i in range(n):
        for j in range(n):
            if board.grid[i][j] != 0 and board.grid[i][j] != i * n + j + 1:
                distance += 1
    return distance

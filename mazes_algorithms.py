import random

import numpy as np


def find_path(grid, i, j, walls: dict):
    if i not in range(0, len(grid)) or j not in range(0, len(grid[i])):
        return
    elif grid[i][j] == 2:
        print(np.array(grid))
        return
    elif grid[i][j] == -1:
        return
    else:
        grid[i][j] = -1
        find_path(grid, i + 1, j, walls)
        find_path(grid, i, j + 1, walls)
        find_path(grid, i - 1, j, walls)
        find_path(grid, i, j - 1, walls)
        grid[i][j] = 0



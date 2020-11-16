import json
import random
from typing import List

import numpy as np
import pygame

# pygame.init()
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
size = 10
grid = [[0 for i in range(size)] for j in range(size)]
width = 16
windows_size = (512, 512)


# screen = pygame.display.set_mode(windows_size, pygame.RESIZABLE)


def draw_maze(grid, walls):
    clear_screen('white', screen)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if walls[y][x]['r']:
                point = (
                    (width + width * x),
                    width + width * y
                )
                pygame.draw.line(screen,
                                 'black',
                                 point,
                                 (
                                     (width + width * x),
                                     width + width + width * y
                                 )
                                 )
            if walls[y][x]['d']:
                point = (
                    (width * x),
                    width + width + width * y
                )
                pygame.draw.line(screen,
                                 'black',
                                 point,
                                 (
                                     (width + width * x),
                                     width + width + width * y
                                 )
                                 )
    update(clock)


def update(clock):
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)


def clear_screen(WHITE, screen):
    screen.fill(WHITE)


def generate_maze(grid: list, i, j, visited: dict, walls: dict):
    # draw_maze(grid, walls)
    if i not in range(len(grid)) or j not in range(len(grid[i])) or visited[i][j]:
        return
    visited[i][j] = True
    order_of_visiting = [(i, j + 1, 'r'), (i, j - 1, 'l'), (i + 1, j, 'd'), (i - 1, j, 'u')]
    random.shuffle(order_of_visiting)
    inverse = {'l': 'r', 'r': 'l', 'u': 'd', 'd': 'u'}
    for n_i, n_j, n_d in order_of_visiting:
        if n_i in range(0, len(grid)) and n_j in range(0, len(grid[n_i])) and not visited[n_i][n_j]:
            walls[i][j][n_d] = False
            walls[n_i][n_j][inverse[n_d]] = False
            generate_maze(grid, n_i, n_j, visited, walls)


def try_something(grid, walls):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Open a new window
    pygame.display.set_caption("My First Game")

    # The loop will carry on until the user exit the game (e.g. clicks the close button).
    carry_on = True

    # -------- Main Program Loop -----------
    while carry_on:
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                carry_on = False  # Flag that we are done so we exit this loop

        # --- Drawing code should go here
        # First, clear the screen to white.
        clear_screen(WHITE, screen)

        line_width = 5

        draw_maze(grid, walls)

        update(clock)

    # Once we have exited the main program loop we can stop the game engine:
    pygame.quit()


def find_paths(grid, i, j, walls, visited):
    print(np.array(grid))
    if i in range(0, len(grid)) and j in range(0, len(grid[i])) and not visited[i][j]:
        grid[i][j] = 9
        visited[i][j] = True
        if not walls[i][j]['r']:
            find_paths(grid, i, j + 1, walls, visited)
        if not walls[i][j]['l']:
            find_paths(grid, i, j - 1, walls, visited)
        if not walls[i][j]['u']:
            find_paths(grid, i - 1, j, walls, visited)
        if not walls[i][j]['d']:
            find_paths(grid, i + 1, j, walls, visited)


if 1 == 1:
    walls = {i: {j: {d: True for d in ['l', 'r', 'u', 'd']} for j in range(size)} for i in range(size)}
    visited = {i: {j: False for j in range(size)} for i in range(size)}

    # start
    grid[0][0] = 1

    # end
    grid[-1][-1] = 2

    generate_maze(grid, 0, 0, visited, walls)

    print(np.array(grid))

    visited = {i: {j: False for j in range(size)} for i in range(size)}

    find_paths(grid, 0, 0, walls, visited)

    print(np.array(grid))

    # try_something(grid, walls)

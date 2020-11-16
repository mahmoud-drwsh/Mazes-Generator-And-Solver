import random
import sys
from math import sqrt

import numpy
import numpy as np
import pygame

size = 16
grid = [[0 for j in range(size)] for i in range(size)]
walls = {i: {j: {d: True for d in ['n', 'e', 's', 'w']} for j in range(size)} for i in range(size)}
visited = {i: {j: False for j in range(size)} for i in range(size)}

inverse = {'w': 'e', 'e': 'w', 'n': 's', 's': 'n'}

# for determining whether the start is being selected or the finish
start_picked = False

# pygame variables
width = 32
padding = 16
display_dimension_width = padding + width * size + padding
display_dimension_height = padding + width * size + padding

# pygame
pygame.init()
screen = pygame.display.set_mode([display_dimension_width, display_dimension_height])
clock = pygame.time.Clock()


def find_path(i, j):
    if i not in range(0, len(grid)) or j not in range(0, len(grid[i])):
        return
    elif grid[i][j] == 2:
        print(np.array(grid))
        return
    elif grid[i][j] == -1:
        return
    else:
        grid[i][j] = -1
        find_path(i + 1, j)
        find_path(i, j + 1)
        find_path(i - 1, j)
        find_path(i, j - 1)
        grid[i][j] = 0


def find_path_in_maze(i, j):
    if i not in range(len(grid)) or j not in range(len(grid[i])) or visited[i][j]:
        return
    if i == size - 1 and j == size - 1:
        print(numpy.array(grid))

    visited[i][j] = True

    neighbors = [
        (i, j + 1, walls[i][j]['e']),
        (i, j - 1, walls[i][j]['w']),
        (i - 1, j, walls[i][j]['n']),
        (i + 1, j, walls[i][j]['s'])
    ]

    for ni, nj, wall in neighbors:
        if not wall and not visited[ni][nj]:
            if ni in range(len(grid)) and nj in range(len(grid[ni])):
                grid[ni][nj] = '|'
                print(numpy.array(grid))
                find_path_in_maze(nj, ni)


def generate_maze(i, j):
    if i not in range(len(grid)) or j not in range(len(grid[i])) or visited[i][j]:
        return
    visited[i][j] = True
    order_of_visiting = [(i, j + 1, 'e'), (i, j - 1, 'w'), (i + 1, j, 's'), (i - 1, j, 'n')]
    random.shuffle(order_of_visiting)
    for n_i, n_j, n_d in order_of_visiting:
        if n_i in range(0, len(grid)) and n_j in range(0, len(grid[n_i])) and not visited[n_i][n_j]:
            walls[i][j][n_d] = False
            walls[n_i][n_j][inverse[n_d]] = False
            draw_maze()
            generate_maze(n_i, n_j)


def setup_maze():
    global visited, grid
    visited = {i: {j: False for j in range(size)} for i in range(size)}
    generate_maze(0, 0)


def draw_maze():
    screen.fill('white')
    for y in range(size):
        for x in range(size):
            # top-right
            top_right = (padding + width + width * x, padding + width * y)
            # bottom-right
            bottom_right = (padding + width + width * x, padding + width + width * y)
            # bottom-left
            bottom_left = (padding + width * x, padding + width + width * y)
            # top-left
            top_left = (padding + width * x, padding + width * y)
            # rectangle coordinates
            rect = (padding + width * x + 1, padding + width * y + 1)

            if grid[y][x] == 1:
                pygame.draw.rect(screen, 'green', rect + (width - 1, width - 1))
            if grid[y][x] == 2:
                pygame.draw.rect(screen, 'red', rect + (width - 1, width - 1))

            if walls[y][x]['e']:
                pygame.draw.line(screen, 'black', top_right, bottom_right)
            if walls[y][x]['s']:
                pygame.draw.line(screen, 'black', bottom_left, bottom_right)
            if x == 0:
                pygame.draw.line(screen, 'black', top_left, bottom_left)
            if y == 0:
                pygame.draw.line(screen, 'black', top_left, top_right)

    pygame.display.update()
    clock.tick(512)


if __name__ == '__main__':
    setup_maze()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x > 123:
                    grid[((y - padding) // width)][((x - padding) // width)] = 2
                else:
                    grid[((y - padding) // width)][((x - padding) // width)] = 1

        screen.fill('white')

        draw_maze()

        pygame.display.update()
        clock.tick(60)

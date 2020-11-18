import collections
import heapq
import queue
from math import sqrt
from time import time

import pygame
import random
import sys

from pygame import font

from mazes.button import button

# the size of the maze
size = 25

# the width of each cell
width = 23

# the width of a maze's cells' walls
line_width = 1

# for determining whether the steps of generation are to be shown
show_map_generation_steps = False

# for determining whether to generate a maze or not
generate_maze = False

# background color
fill_color = 'black'

# walls color
walls_color = 'white'

# the size of the maze in both the horizontal direction as well as the vertical
# the grid which will hold information about the maze
grid = [[0 for j in range(size)] for i in range(size)]

# for determining which algorithm to use for finding the path
# 1 -> Simple DFS
# 2 -> Dijkstra's algorithm
# 3 -> A* algorithm
algorithm = 3


# a dictionary of the coordinates and the walls to their cardinal directions
walls = {i: {j: {d: generate_maze for d in ['n', 'e', 's', 'w']} for j in range(size)} for i in range(size)}

# cardinal directions' inverses
directions_inverses = {'w': 'e', 'e': 'w', 'n': 's', 's': 'n'}

# the speed of drawing the path
path_drawing_speed = 512

# for determining whether the start is being selected or the finish
start_picked = False
# will hold the coordinates of the starting point
start = ()
# will hold the coordinates of the goal point
goal = ()

# the padding to the 4 corners of the maze
padding = 8
# the window's dimensions
display_dimension_width = 2 * padding + width * size
display_dimension_height = 2 * padding + width * size + width * 2

# initiating the canvas's windows
pygame.init()
# creating a canvas
screen = pygame.display.set_mode([display_dimension_width, display_dimension_height])
pygame.display.set_caption('maze generator')
# the clock object which specifies how fast the screen updates
clock = pygame.time.Clock()


def visited_mappings():
    return {i: {j: False for j in range(size)} for i in range(size)}


def get_neighbours(i, j, with_walls=True):
    if with_walls:
        neighbors = [
            (i, j + 1, walls[i][j]['e']),
            (i, j - 1, walls[i][j]['w']),
            (i - 1, j, walls[i][j]['n']),
            (i + 1, j, walls[i][j]['s'])
        ]
    else:
        neighbors = [
            (i, j + 1),
            (i, j - 1),
            (i - 1, j),
            (i + 1, j)
        ]

    return neighbors


def valid(ni, nj, matrix):
    return ni in range(len(matrix)) and nj in range(len(matrix[ni]))


def generate_maze(i, j, visited, draw_steps=False):
    if draw_steps:
        draw_maze()

    if not valid(i, j, visited) or visited[i][j]:
        return
    visited[i][j] = True
    order_of_visiting = [(i, j + 1, 'e'), (i, j - 1, 'w'), (i + 1, j, 's'), (i - 1, j, 'n')]
    random.shuffle(order_of_visiting)
    for n_i, n_j, n_d in order_of_visiting:
        if n_i in range(0, len(grid)) and n_j in range(0, len(grid[n_i])) and not visited[n_i][n_j]:
            walls[i][j][n_d] = False
            walls[n_i][n_j][directions_inverses[n_d]] = False

            grid[i][j] = 3
            grid[n_i][n_j] = 3

            generate_maze(n_i, n_j, visited, show_map_generation_steps)

            grid[n_i][n_j] = 0
            grid[i][j] = 0

            if draw_steps:
                draw_maze()


def setup_maze():
    # generate_maze(size // 2, size // 2, visited_mappings(), show_map_generation_steps)
    generate_maze(0, 0, visited_mappings(), show_map_generation_steps)


def dfs_find_path_in_maze(i, j, maze_grid, visited):
    frame_rate = 60

    if not valid(i, j, visited) or visited[i][j]:
        return False
    if maze_grid[i][j] == 2:
        return True

    visited[i][j] = True

    draw_maze(frame_rate)

    if not (i == start[0] and j == start[1]):
        maze_grid[i][j] = 3

    neighbors = get_neighbours(i, j)

    for ni, nj, wall in neighbors:

        if valid(ni, nj, maze_grid) and not wall and not visited[ni][nj]:
            if dfs_find_path_in_maze(ni, nj, maze_grid, visited):
                return True

    maze_grid[i][j] = 0

    draw_maze(frame_rate)


def bfs_on_maze(i, j, maze_grid, visited, path_drawing_speed=30):
    frontier = collections.deque()

    parents = {}

    frontier.append((i, j))

    path = collections.deque()

    dest_i, dest_j = None, None

    while frontier:
        curr_ni, curr_nj = frontier.popleft()

        if visited[curr_ni][curr_nj]:
            continue

        draw_maze()

        if maze_grid[curr_ni][curr_nj] == 2:
            dest_i, dest_j = curr_ni, curr_nj
            break

        visited[curr_ni][curr_nj] = True

        if maze_grid[curr_ni][curr_nj] != 1:
            maze_grid[curr_ni][curr_nj] = 3

        neighbours = get_neighbours(curr_ni, curr_nj)

        for ni, nj, wall in neighbours:
            if valid(ni, nj, visited) and not visited[ni][nj] and not wall:
                parents[(ni, nj)] = (curr_ni, curr_nj)
                frontier.append((ni, nj))

    draw_path(dest_i, dest_j, maze_grid, parents, path, path_drawing_speed)


def manhattan_distance(i, j, goal):
    return sqrt(abs(goal[0] - i) ** 2 + abs(goal[1] - j) ** 2)


def a_star_search(i, j, maze_grid, visited, path_drawing_speed=path_drawing_speed):
    frontier = []

    parents = {}

    heapq.heappush(frontier, (manhattan_distance(i, j, goal), i, j))

    path = collections.deque()

    dest_i, dest_j = None, None

    while len(frontier) > 0:
        dist, curr_ni, curr_nj = heapq.heappop(frontier)

        if visited[curr_ni][curr_nj]:
            continue

        if maze_grid[curr_ni][curr_nj] == 2:
            dest_i, dest_j = curr_ni, curr_nj
            break

        visited[curr_ni][curr_nj] = True

        if maze_grid[curr_ni][curr_nj] != 1:
            maze_grid[curr_ni][curr_nj] = 3

        draw_maze()

        neighbours = get_neighbours(curr_ni, curr_nj)

        for ni, nj, wall in neighbours:
            if valid(ni, nj, visited) and not visited[ni][nj] and not wall:
                parents[(ni, nj)] = (curr_ni, curr_nj)
                heapq.heappush(frontier, (manhattan_distance(ni, nj, goal), ni, nj))

    draw_path(dest_i, dest_j, maze_grid, parents, path, path_drawing_speed)


def put_into_priority_queue(frontier: queue.PriorityQueue, i, j, goal):
    frontier.put((manhattan_distance(i, j, goal), i, j))


def draw_maze(frame_rate=10240):
    react_to_events()

    screen.fill(fill_color)

    draw_button(0, 'DFS')
    draw_button(1, "BFS")
    draw_button(2, "A*")

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

            rect_padding = 1

            # rectangle coordinates
            rect = (padding + width * x + rect_padding, padding + width * y + rect_padding)

            # circle information
            circle_radius = (width // 2) - line_width * 1.5

            circle_center = (
                padding + (width * x) + (width // 2) + line_width,
                padding + (width * y) + (width // 2) + line_width)

            # circle_center = (
            #     padding + (width * x) + (width // 2),
            #     padding + (width * y) + (width // 2))

            color = '#ff1744'

            if grid[y][x] == 1:
                color = '#66bb6a'
            if grid[y][x] == 2:
                color = '#c30000'
            if grid[y][x] == 3:
                color = '#2196f3'
            if grid[y][x] == 4:
                color = '#aa00ff'

            if grid[y][x] != 0:
                # pygame.draw.rect(screen, color, rect + (width - rect_padding * 2, width - rect_padding * 2), 0)
                pygame.draw.circle(screen, color, circle_center, circle_radius)

            if walls[y][x]['e']:
                pygame.draw.line(screen, walls_color, top_right, bottom_right, line_width)
            if walls[y][x]['s']:
                pygame.draw.line(screen, walls_color, bottom_left, bottom_right, line_width)
            if x == 0:
                pygame.draw.line(screen, walls_color, top_left, bottom_left, line_width)
            if x == size - 1:
                pygame.draw.line(screen, walls_color, top_right, bottom_right, line_width)
            if y == 0:
                pygame.draw.line(screen, walls_color, top_left, top_right, line_width)
            if y == size - 1:
                pygame.draw.line(screen, walls_color, bottom_left, bottom_right, line_width)

    pygame.display.update()
    clock.tick(frame_rate)


def draw_button(button_number, text='hello'):
    x_coordinate = padding + (display_dimension_width // 3) * button_number
    y_coordinate = display_dimension_height - width * 2
    rect_width = ((display_dimension_width - padding * 2) // 3) - padding
    rect_height = width * 2 - padding

    pygame.draw.rect(
        screen,
        walls_color,
        [x_coordinate,
         y_coordinate,
         rect_width,
         rect_height
         ]
    )

    color = 'black'
    f = font.SysFont(None, width * 2).render(text, True, color)
    screen.blit(f, (x_coordinate + (rect_width // 3), y_coordinate))


def draw_path(dest_i, dest_j, maze_grid, parents, path, path_drawing_speed):
    if dest_i is not None and dest_j is not None:
        curr = (dest_i, dest_j)
        path += [curr]
        while parents.__contains__(curr):
            path += [parents[curr]]
            curr = parents[curr]
    path.reverse()
    for i in range(size):
        for j in range(size):
            if maze_grid[i][j] == 3:
                maze_grid[i][j] = 0
    for i, j in path:
        if maze_grid[i][j] not in range(1, 3):
            maze_grid[i][j] = 4
            draw_maze(path_drawing_speed)


def react_to_events():
    global start_picked, grid, start, goal, algorithm

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:

            x, y = pygame.mouse.get_pos()
            i = ((y - padding) // width)
            j = ((x - padding) // width)

            if clicked_within_the_maze(x, y):

                if start_picked:
                    grid[i][j] = 2

                    goal = (i, j)

                    start_picked = not start_picked

                    i, j = start

                    if algorithm == 1:
                        pygame.display.set_caption('A maze generator and solver using depth-first search')
                        dfs_find_path_in_maze(i, j, grid, visited_mappings())
                    elif algorithm == 2:
                        pygame.display.set_caption("A maze generator and solver using Dijkstra's algorithm")
                        bfs_on_maze(i, j, grid, visited_mappings())
                    elif algorithm == 3:
                        pygame.display.set_caption("A maze generator and solver using A* algorithm")
                        a_star_search(i, j, grid, visited_mappings())

                else:
                    grid = [[0 for j in range(size)] for i in range(size)]
                    grid[i][j] = 1
                    start_picked = not start_picked
                    start = (i, j)

            else:
                third = display_dimension_width // 3
                region = x // third
                if region == 0:
                    algorithm = 1
                elif region == 1:
                    algorithm = 2
                elif region == 2:
                    algorithm = 3


def clicked_within_the_maze(x, y):
    return y in range(padding, padding + size * width) and x in range(padding, padding + size * width)


if __name__ == '__main__':
    setup_maze()

    while True:
        react_to_events()

        screen.fill(fill_color)

        button('black', 100, 100, 0, 0)

        draw_maze()

        pygame.display.update()
        clock.tick(30)

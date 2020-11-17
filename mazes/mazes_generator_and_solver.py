import collections

import pygame
import random
import sys

from mazes.button import button

size = 10

# the size of the maze in both the horizontal direction as well as the vertical
# the grid which will hold information about the maze
grid = [[0 for j in range(size)] for i in range(size)]

# for determining which algorithm to use for finding the path
# 1 -> Dijkstra's algorithm
# 2 -> Simple DFS
algorithm = 2

# a dictionary of the coordinates and the walls to their cardinal directions
walls = {i: {j: {d: True for d in ['n', 'e', 's', 'w']} for j in range(size)} for i in range(size)}

# cardinal directions' inverses
directions_inverses = {'w': 'e', 'e': 'w', 'n': 's', 's': 'n'}

# for determining whether the steps of generation are to be shown
show_map_generation_steps = False

# the speed of drawing the path
path_drawing_speed = 128

# for determining whether the start is being selected or the finish
start_picked = False
# will hold the coordinates of the starting point
start = ()

# the width of a maze's cell
width = 25

# the padding to the 4 corners of the maze
padding = 8
# the window's dimensions
display_dimension_width = padding + width * size + padding
display_dimension_height = padding + width * size + padding

# initiating the canvas's windows
pygame.init()
# creating a canvas
screen = pygame.display.set_mode([display_dimension_width, display_dimension_height])
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


def find_path_in_maze(i, j, maze_grid, visited):
    if i not in range(0, len(maze_grid)) or j not in range(0, len(maze_grid[i])) or visited[i][j]:
        return False
    if maze_grid[i][j] == 2:
        draw_maze()
        return True

    visited[i][j] = True

    draw_maze()

    if not (i == start[0] and j == start[1]):
        maze_grid[i][j] = 3

    neighbors = get_neighbours(i, j)

    for ni, nj, wall in neighbors:

        if valid(ni, nj, visited) and not wall and not visited[ni][nj]:
            if ni in range(len(maze_grid)) and nj in range(len(maze_grid[ni])):
                if find_path_in_maze(ni, nj, maze_grid, visited):
                    return True

    maze_grid[i][j] = 0


def generate_maze(i, j, visited, draw_steps=False):
    if draw_steps:
        draw_maze()
    if i not in range(len(grid)) or j not in range(len(grid[i])) or visited[i][j]:
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
    generate_maze(size // 2, size // 2, visited_mappings(), show_map_generation_steps)


def draw_maze(frame_rate=99999):
    react_to_events()

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

            rect_padding = 5

            # rectangle coordinates
            rect = (padding + width * x + rect_padding, padding + width * y + rect_padding)

            color = 'green'

            if grid[y][x] == 1:
                color = 'green'
            if grid[y][x] == 2:
                color = 'red'
            if grid[y][x] == 3:
                color = 'yellow'
            if grid[y][x] == 4:
                color = 'purple'

            if grid[y][x] != 0:
                pygame.draw.rect(screen, color, rect + (width - rect_padding, width - rect_padding), 0)

            if walls[y][x]['e']:
                pygame.draw.line(screen, 'black', top_right, bottom_right)
            if walls[y][x]['s']:
                pygame.draw.line(screen, 'black', bottom_left, bottom_right)
            if x == 0:
                pygame.draw.line(screen, 'black', top_left, bottom_left)
            if y == 0:
                pygame.draw.line(screen, 'black', top_left, top_right)

    pygame.display.update()
    clock.tick(frame_rate)


def valid(ni, nj, visited):
    return ni in range(len(visited)) and nj in range(len(visited[ni]))


def bfs_on_maze(i, j, maze_grid, visited, path_drawing_speed=30):
    frontier = collections.deque()

    parents = {}

    frontier += [(i, j)]

    path = collections.deque()

    dest_i, dest_j = None, None

    while frontier:
        curr_ni, curr_nj = frontier.popleft()

        if maze_grid[curr_ni][curr_nj] == 2:
            dest_i, dest_j = curr_ni, curr_nj
            break

        visited[curr_ni][curr_nj] = True

        if maze_grid[curr_ni][curr_nj] != 1:
            maze_grid[curr_ni][curr_nj] = 3

        draw_maze()

        neighbours = get_neighbours(curr_ni, curr_nj)

        for ni, nj, wall in neighbours:
            if valid(ni, nj, visited):
                if not visited[ni][nj] and not wall:
                    parents[(ni, nj)] = (curr_ni, curr_nj)
                    frontier += [(ni, nj)]

    if dest_i is not None and dest_j is not None:
        curr = (dest_i, dest_j)
        path += [curr]
        while parents.__contains__(curr):
            path += [parents[curr]]
            curr = parents[curr]

    path.reverse()

    for i, j in path:
        if maze_grid[i][j] not in range(1, 3):
            maze_grid[i][j] = 4
            draw_maze(path_drawing_speed)

    for i in range(size):
        for j in range(size):
            if maze_grid[i][j] == 3:
                maze_grid[i][j] = 0
    pass


def react_to_events():
    global start_picked, grid, start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            i = ((y - padding) // width)
            j = ((x - padding) // width)

            if y in range(padding, padding + size * width) and x in range(padding, padding + size * width):
                if start_picked:
                    grid[i][j] = 2
                    start_picked = not start_picked

                    i, j = start

                    if algorithm == 1:
                        pygame.display.set_caption('A maze generator and solver using depth-first search')
                        find_path_in_maze(i, j, grid, visited_mappings())
                    elif algorithm == 2:
                        pygame.display.set_caption("A maze generator and solver using Dijkstra's algorithm")
                        bfs_on_maze(i, j, grid, visited_mappings())
                else:
                    grid = [[0 for j in range(size)] for i in range(size)]
                    grid[i][j] = 1
                    start_picked = not start_picked
                    start = (i, j)


if __name__ == '__main__':
    setup_maze()

    while True:
        react_to_events()

        screen.fill('white')

        button('black', 100, 100, 0, 0)

        draw_maze()

        pygame.display.update()
        clock.tick(30)

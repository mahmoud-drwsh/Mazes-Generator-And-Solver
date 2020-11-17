import collections

import pygame
import random
import sys


def visited_mappings():
    return {i: {j: False for j in range(size)} for i in range(size)}


size = 16
grid = [[0 for j in range(size)] for i in range(size)]

algo = 2

walls = {i: {j: {d: True for d in ['n', 'e', 's', 'w']} for j in range(size)} for i in range(size)}

inverse = {'w': 'e', 'e': 'w', 'n': 's', 's': 'n'}

# for determining whether the start is being selected or the finish
start_picked = False
start = ()

# pygame variables
width = 32
padding = 8
display_dimension_width = padding + width * size + padding
display_dimension_height = padding + width * size + padding

# pygame
pygame.init()
pygame.display.set_caption('A maze generator and solver using depth-first search')
screen = pygame.display.set_mode([display_dimension_width, display_dimension_height])
clock = pygame.time.Clock()


def get_neighbours(i, j):
    neighbors = [
        (i, j + 1, walls[i][j]['e']),
        (i, j - 1, walls[i][j]['w']),
        (i - 1, j, walls[i][j]['n']),
        (i + 1, j, walls[i][j]['s'])
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

        if not wall and not visited[ni][nj]:
            if ni in range(len(maze_grid)) and nj in range(len(maze_grid[ni])):
                if find_path_in_maze(ni, nj, maze_grid, visited):
                    return True

    maze_grid[i][j] = 0


def generate_maze(i, j, visited):
    draw_maze(200)
    if i not in range(len(grid)) or j not in range(len(grid[i])) or visited[i][j]:
        return
    visited[i][j] = True
    order_of_visiting = [(i, j + 1, 'e'), (i, j - 1, 'w'), (i + 1, j, 's'), (i - 1, j, 'n')]
    random.shuffle(order_of_visiting)
    for n_i, n_j, n_d in order_of_visiting:
        if n_i in range(0, len(grid)) and n_j in range(0, len(grid[n_i])) and not visited[n_i][n_j]:
            walls[i][j][n_d] = False
            walls[n_i][n_j][inverse[n_d]] = False

            grid[i][j] = 3
            grid[n_i][n_j] = 3

            generate_maze(n_i, n_j, visited)

            grid[n_i][n_j] = 0
            grid[i][j] = 0


def setup_maze():
    generate_maze(size // 2, size // 2, visited_mappings())


def draw_maze(frame_rate=9000):
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

            # rectangle coordinates
            rect = (padding + width * x + 1, padding + width * y + 1)

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
                pygame.draw.rect(screen, color, rect + (width - 2, width - 2))

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


def bfs_on_maze(i, j, maze_grid, visited):
    q = collections.deque()

    parents = {}

    q += [(i, j)]

    dest_i, dest_j = None, None

    while q:
        curr_ni, curr_nj = q.popleft()

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
                    q += [(ni, nj)]

    path = collections.deque()

    if dest_i is not None and dest_j is not None:
        curr = (dest_i, dest_j)
        path += [curr]
        while parents.__contains__(curr):
            path += [parents[curr]]
            curr = parents[curr]

    for i, j in path:
        if maze_grid[i][j] not in range(1, 3):
            maze_grid[i][j] = 4
            draw_maze(16)

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

                    if algo == 1:
                        find_path_in_maze(i, j, grid, visited_mappings())
                    elif algo == 2:
                        pygame.display.set_caption('A maze generator and solver using BFS search')
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

        draw_maze()

        pygame.display.update()
        clock.tick(30)

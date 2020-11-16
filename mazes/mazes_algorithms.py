import pygame
import random
import sys


def initialize_visited():
    return {i: {j: False for j in range(size)} for i in range(size)}


size = 32
grid = [[0 for j in range(size)] for i in range(size)]

walls = {i: {j: {d: True for d in ['n', 'e', 's', 'w']} for j in range(size)} for i in range(size)}

visited = initialize_visited()

inverse = {'w': 'e', 'e': 'w', 'n': 's', 's': 'n'}

# for determining whether the start is being selected or the finish
start_picked = False
start = ()

# pygame variables
width = 19
padding = 8
display_dimension_width = padding + width * size + padding
display_dimension_height = padding + width * size + padding

# pygame
pygame.init()
pygame.display.set_caption('A maze generator and solver using depth-first search')
screen = pygame.display.set_mode([display_dimension_width, display_dimension_height])
clock = pygame.time.Clock()


def find_path_in_maze(i, j, grid, visited):
    if i not in range(0, len(grid)) or j not in range(0, len(grid[i])) or visited[i][j]:
        return False
    if grid[i][j] == 2:
        draw_maze()
        return True

    visited[i][j] = True

    draw_maze()

    if not (i == start[0] and j == start[1]):
        grid[i][j] = 3

    neighbors = [
        (i, j + 1, walls[i][j]['e']),
        (i, j - 1, walls[i][j]['w']),
        (i - 1, j, walls[i][j]['n']),
        (i + 1, j, walls[i][j]['s'])
    ]

    for ni, nj, wall in neighbors:

        if not wall and not visited[ni][nj]:
            if ni in range(len(grid)) and nj in range(len(grid[ni])):
                if find_path_in_maze(ni, nj, grid, visited):
                    return True

    grid[i][j] = 0


def generate_maze(i, j, visited):
    draw_maze()
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
    visited = initialize_visited()
    generate_maze(0, 0, visited.copy())


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

            if grid[y][x] == 1:
                pygame.draw.rect(screen, 'green', rect + (width - 1, width - 1))
            if grid[y][x] == 2:
                pygame.draw.rect(screen, 'red', rect + (width - 1, width - 1))
            if grid[y][x] == 3:
                pygame.draw.rect(screen, 'yellow', rect + (width - 1, width - 1))

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


def react_to_events():
    global start_picked, visited, grid, start
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

                    visited = initialize_visited()
                    find_path_in_maze(i, j, grid, visited)
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

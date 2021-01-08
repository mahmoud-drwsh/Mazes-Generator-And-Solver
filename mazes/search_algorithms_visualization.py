import collections
import heapq
import pygame
import random
import sys

from Maze import Maze
from button import Button

# the maze dimensions
maze_width = 60
maze_height = int(maze_width / 16 * 7.5)

# the maze
maze = Maze(maze_width, maze_height)

# the width of each cell
width = 23

# the width of a maze's cells' walls
line_width = 2

# show a wall-less maze instead
drop_maze_walls = False

# drop all walls
maze.clear_all_walls(drop_maze_walls)

# for determining whether the steps of generation are to be shown
show_map_generation_steps = False

# show the steps of search
show_search_steps = True

# background color
fill_color = 'black'

# walls color
walls_color = 'white'

# for determining which algorithm to use for finding the path
# 1 -> Simple DFS
# 2 -> Dijkstra's algorithm
# 3 -> A* algorithm
algorithm = 3

# the speed of drawing the path
path_drawing_speed = 102400

# the padding to the 4 corners of the maze
padding = 8
# the window's dimensions
display_dimension_width = width * maze.width
display_dimension_height = width * maze.height + width * 2 + padding

# initiating the canvas's windows
pygame.init()
# creating a canvas
screen = pygame.display.set_mode(
    [display_dimension_width, display_dimension_height])
pygame.display.set_caption('Random Maze Generator By Mahmoud Darwish')
# the clock object which specifies how fast the screen updates
clock = pygame.time.Clock()

show_buttons = True


def generate_maze(i, j, draw_steps=False):
    if draw_steps:
        draw_maze()

    if maze.is_valid_cell(i, j) and not maze.visited_cell(i, j):

        maze.mark_cell_visited(i, j)

        neighbours = maze.get_cell_neighbours_and_directions(i, j)
        random.shuffle(neighbours)

        for neighbour_i, neighbour_j, neighbour_direction in neighbours:

            if maze.is_valid_cell(
                neighbour_i, neighbour_j
            ) and not maze.visited_cell(neighbour_i, neighbour_j):

                maze.remove_the_wall_between_cells(
                    i, j, neighbour_direction)

                # to show where the generator has reached
                maze.grid[i][j] = Maze.SEARCHED_CELL
                maze.grid[neighbour_i][neighbour_j] = Maze.SEARCHED_CELL

                generate_maze(neighbour_i, neighbour_j,
                              show_map_generation_steps)

                # backtrack
                maze.grid[neighbour_i][neighbour_j] = Maze.EMPTY_CELL
                maze.grid[i][j] = Maze.EMPTY_CELL

                if draw_steps:
                    draw_maze()


def generate_maze_iteratively(i, j, draw_steps=False):
    # iterative
    if not maze.is_valid_cell(i, j) or maze.visited_cell(i, j):

        return
    stack = [(i, j)]

    while stack:
        if draw_steps:
            draw_maze()

        i, j = stack.pop()

        # show that the cell has been removed from the stack
        maze.grid[i][j] = Maze.EMPTY_CELL

        maze.mark_cell_visited(i, j)

        neighbours = [neighbour for neighbour in maze.get_cell_neighbours_and_directions(i, j)
                      if
                      maze.is_valid_cell(neighbour[0], neighbour[1]) and
                      not maze.visited_cell(neighbour[0], neighbour[1])
                      ]

        random.shuffle(neighbours)

        for neighbour_i, neighbour_j, neighbour_direction in neighbours:
            if maze.is_valid_cell(
                neighbour_i, neighbour_j
            ) and not maze.visited_cell(neighbour_i, neighbour_j):
                stack.append((i, j))

                # show that the cell is in the stack
                maze.grid[i][j] = Maze.SEARCHED_CELL

                maze.remove_the_wall_between_cells(
                    i, j, neighbour_direction)

                maze.mark_cell_visited(neighbour_i, neighbour_j)

                stack.append((neighbour_i, neighbour_j))

                break


def setup_maze():
    maze.reconstruct_walls_and_clear_grid(drop_maze_walls)
    generate_maze_iteratively(1, 1, show_map_generation_steps)


def dfs_find_path_in_maze(i, j):
    if not maze.is_valid_cell(i, j) or maze.visited_cell(i, j) or \
            maze.start_picked or maze.grid[i][j] == Maze.WALL_CELL:
        return False
    if maze.grid[i][j] == Maze.GOAL_CELL:
        return True

    maze.mark_cell_visited(i, j)

    if show_search_steps:
        draw_maze()

    if maze.grid[i][j] != Maze.START_CELL:
        maze.grid[i][j] = Maze.SEARCHED_CELL

    neighbors = maze.get_cell_search_neighbours(i, j)

    for ni, nj, wall in neighbors:

        if (
            maze.is_valid_cell(ni, nj)
            and not wall
            and not maze.visited_cell(ni, nj)
            and dfs_find_path_in_maze(ni, nj)
        ):
            if maze.grid[i][j] != Maze.START_CELL:
                maze.grid[i][j] = Maze.PATH_CELL
            return True

    maze.grid[i][j] = Maze.EMPTY_CELL

    # if show_search_steps:
    #     draw_maze()


def bfs_on_maze(i, j):
    frontier = collections.OrderedDict()

    parents = {}

    frontier[(i, j)] = None

    dest_i, dest_j = None, None

    while frontier and not maze.start_picked:
        key, _val = frontier.popitem(False)
        curr_ni, curr_nj = key

        if maze.visited_cell(curr_ni, curr_nj):
            continue

        maze.mark_cell_visited(curr_ni, curr_nj)

        if show_search_steps:
            draw_maze()

        if maze.grid[curr_ni][curr_nj] == Maze.GOAL_CELL:
            dest_i, dest_j = curr_ni, curr_nj
            break

        if maze.grid[curr_ni][curr_nj] != Maze.START_CELL:
            maze.grid[curr_ni][curr_nj] = Maze.SEARCHED_CELL

        neighbours = maze.get_cell_search_neighbours(curr_ni, curr_nj)

        for ni, nj, wall in neighbours:
            if maze.is_valid_cell(ni, nj) and not maze.visited_cell(ni, nj) and not wall:
                parents[(ni, nj)] = (curr_ni, curr_nj)
                frontier[(ni, nj)] = None

    draw_path(dest_i, dest_j, parents)


def a_star_search(i, j):
    frontier = []

    parents = {}

    heapq.heappush(frontier, (maze.distance_to_goal(i, j), i, j))

    dest_i, dest_j = None, None

    while frontier and not maze.start_picked:
        dist, curr_ni, curr_nj = heapq.heappop(frontier)

        if maze.visited_cell(curr_ni, curr_nj):
            continue

        if maze.grid[curr_ni][curr_nj] == Maze.GOAL_CELL:
            dest_i, dest_j = curr_ni, curr_nj
            break

        maze.mark_cell_visited(curr_ni, curr_nj)

        if maze.grid[curr_ni][curr_nj] != Maze.START_CELL:
            maze.grid[curr_ni][curr_nj] = Maze.SEARCHED_CELL

        if show_search_steps:
            draw_maze()

        neighbours = maze.get_cell_search_neighbours(curr_ni, curr_nj)

        for ni, nj, wall in neighbours:
            if maze.is_valid_cell(ni, nj) and not maze.visited_cell(ni, nj) and not wall:
                parents[(ni, nj)] = (curr_ni, curr_nj)
                heapq.heappush(
                    frontier, (maze.distance_to_goal(ni, nj), ni, nj))

    draw_path(dest_i, dest_j, parents)


def draw_maze():
    screen.fill(fill_color)

    if show_buttons:
        buttons = get_drawn_buttons()
        react_to_events(buttons)

    for y in range(maze.height):
        for x in range(maze.width):
            # top-right
            top_right = (padding + width + width * x, padding + width * y)
            # bottom-right
            bottom_right = (padding + width + width * x,
                            padding + width + width * y)
            # bottom-left
            bottom_left = (padding + width * x, padding + width + width * y)
            # top-left
            top_left = (width * x, width * y)

            # rectangle coordinates
            # rect_padding = 1
            # rect = (maze.width * x, maze.height * y)

            # circle information
            circle_radius = (width // 2) - line_width * 1.3
            circle_center = (
                padding + (width * x) + ((width + line_width) // 2),
                padding + (width * y) + ((width + line_width) // 2))

            color = '#ff1744'

            if maze.grid[y][x] == Maze.WALL_CELL:
                color = '#000000'
            if maze.grid[y][x] == Maze.EMPTY_CELL:
                color = '#bdbdbd'
            if maze.grid[y][x] == Maze.SEARCHED_CELL:
                color = '#0277bd'
            if maze.grid[y][x] == Maze.PATH_CELL:
                color = '#4527a0'
            if maze.grid[y][x] == Maze.GOAL_CELL:
                color = 'green'
            if maze.grid[y][x] == Maze.START_CELL:
                color = 'red'

            pygame.draw.rect(screen, color, top_left + (width, width))

            if x == 0 or x == maze.width - 1 or y == 0 or y == maze.height - 1:
                pygame.draw.rect(screen, "#000000", top_left + (width, width))

            # if x == 0 and y == 0:
            #     pygame.draw.rect(screen, "green", top_left + (width, width))

    pygame.display.update()


def get_drawn_buttons():
    buttons = draw_buttons(
        ['DFS', "BFS", "A*", "Regenerate", "Toggle Walls", "Show Steps"])
    [b.draw(screen) for b in buttons]
    return buttons


def draw_buttons(text):
    buttons = []

    for i in range(len(text)):
        x_coordinate = padding + (display_dimension_width // len(text)) * i
        y_coordinate = display_dimension_height - width * 2
        rect_width = ((display_dimension_width - padding) //
                      len(text)) - padding
        rect_height = width * 2 - padding

        buttons += [
            Button(
                'purple'
                if i == algorithm - 1 or (i == 4 and not drop_maze_walls) or (i == 5 and show_search_steps)
                else 'white',
                x_coordinate,
                y_coordinate,
                rect_width,
                rect_height,
                text[i]
            )
        ]

    return buttons


def draw_path(dest_i, dest_j, parents):
    path = collections.deque()

    if dest_i is not None and dest_j is not None:
        curr = (dest_i, dest_j)
        path += [curr]

        while parents.__contains__(curr):
            path += [parents[curr]]
            curr = parents[curr]

    path.reverse()

    for i in range(maze_height):
        for j in range(maze_width):
            if maze.grid[i][j] == Maze.SEARCHED_CELL:
                maze.grid[i][j] = Maze.EMPTY_CELL

    for i, j in path:
        if not maze.start_picked:
            if maze.grid[i][j] not in [Maze.START_CELL, Maze.GOAL_CELL]:
                maze.grid[i][j] = Maze.PATH_CELL

            if show_search_steps:
                draw_maze()


def react_to_events(buttons):
    global algorithm

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            react_to_mouse_click(buttons)


def react_to_mouse_click(buttons):
    global algorithm, drop_maze_walls

    x, y = pygame.mouse.get_pos()

    i = (y // width)
    j = (x // width)

    if clicked_within_the_maze(x, y) and maze.grid[i][j] != Maze.WALL_CELL:

        if maze.start_picked:

            maze.grid[i][j] = Maze.GOAL_CELL

            maze.goal = (i, j)

            maze.start_picked = not maze.start_picked

            i, j = maze.start

            if algorithm == 1:
                pygame.display.set_caption(
                    'A maze generator and solver using depth-first search By Mahmoud Darwish')
                dfs_find_path_in_maze(i, j)
            elif algorithm == 2:
                pygame.display.set_caption(
                    "A maze generator and solver using Dijkstra's algorithm By Mahmoud Darwish")
                bfs_on_maze(i, j)
            elif algorithm == 3:
                pygame.display.set_caption(
                    "A maze generator and solver using A* algorithm By Mahmoud Darwish")
                a_star_search(i, j)

        else:
            maze.start_picked = not maze.start_picked
            maze.mark_all_cells_not_visited()
            maze.clear_grid()
            maze.grid[i][j] = Maze.START_CELL
            maze.start = (i, j)

    elif x in range(width) and y in range(width):
        global show_buttons
        show_buttons = not show_buttons

    else:
        if buttons[0].isOver((x, y)):
            algorithm = 1
        elif buttons[1].isOver((x, y)):
            algorithm = 2
        elif buttons[2].isOver((x, y)):
            algorithm = 3
        elif buttons[3].isOver((x, y)):
            if not drop_maze_walls:
                maze.start_picked = not maze.start_picked
                setup_maze()
        elif buttons[4].isOver((x, y)):
            drop_maze_walls = not drop_maze_walls
            maze.start_picked = not maze.start_picked
            if drop_maze_walls:
                maze.drop_all_walls()
            else:
                setup_maze()
        elif buttons[5].isOver((x, y)):
            global show_search_steps
            show_search_steps = not show_search_steps


def clicked_within_the_maze(x, y):
    return y in range(width, maze_height * width) and x in range(width, maze_width * width)


if __name__ == '__main__':
    setup_maze()

    while True:
        react_to_events(get_drawn_buttons())

        draw_maze()

        pygame.display.update()
        clock.tick(30)

from math import sqrt


class Maze(object):
    # the cardinal directions and their inverses
    NORTH = 'n'
    EAST = 'e'
    SOUTH = 's'
    WEST = 'w'
    directions_inverses = {WEST: EAST, EAST: WEST, NORTH: SOUTH, SOUTH: NORTH}
    cardinal_directions = {NORTH, EAST, SOUTH, WEST}

    EMPTY_CELL = 0
    START_CELL = 1
    GOAL_CELL = 2
    WALL_CELL = 3
    SEARCHED_CELL = 4
    PATH_CELL = 5

    def __init__(self, width, height):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        # self.walls = self.__construct_walls__()
        self.start = ()
        self.goal = ()
        self.start_picked = False
        self.visited = self.__visited_mappings__()
        self.grid = self.__initiate_grid__()
        self.clear_grid()

    def __initiate_grid__(self, with_walls=True):
        if with_walls:
            return [[Maze.WALL_CELL
                     if
                     _j == 0 or
                     _i == 0 or
                     _j == self.width - 1 or
                     _i == self.height - 1 or
                     _i % 2 == 0 or
                     _j % 2 == 0
                     else Maze.EMPTY_CELL
                     for _j in range(self.width)] for _i in range(self.height)]
        else:
            return [[Maze.EMPTY_CELL for _j in range(self.width)] for _i in range(self.height)]

    def __visited_mappings__(self):
        return {i: {j: False for j in range(self.width)} for i in range(self.height)}

    # def __construct_walls__(self, with_walls=True):
    #     return {i: {j: {d: with_walls
    #                     for d in Maze.cardinal_directions
    #                     }
    #                 for j in range(self.width)
    #                 }
    #             for i in range(self.height)
    #             }

    def mark_all_cells_not_visited(self):
        self.visited = self.__visited_mappings__()

    def reconstruct_walls_and_clear_grid(self, without_walls=False):
        self.grid = self.__initiate_grid__()
        # self.walls = self.__construct_walls__(not without_walls)
        self.visited = self.__visited_mappings__()

    def clear_grid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j] = Maze.EMPTY_CELL if self.grid[i][j] != Maze.WALL_CELL else self.grid[i][j]

    def clean_grid_mark_all_cells_not_visited(self):
        self.grid = self.__initiate_grid__()
        self.mark_all_cells_not_visited()

    def clear_all_walls(self, without_walls=False):
        self.drop_all_walls()

    def get_cell_neighbours(self, i, j, with_walls=True):
        if with_walls:
            return [
                (i, j + 2, self.grid[i][j + 1] == Maze.WALL_CELL),
                (i, j - 2, self.grid[i][j - 1] == Maze.WALL_CELL),
                (i - 2, j, self.grid[i - 1][j] == Maze.WALL_CELL),
                (i + 2, j, self.grid[i + 1][j] == Maze.WALL_CELL)
            ]
        else:
            return [
                (i, j + 1),
                (i, j - 1),
                (i - 1, j),
                (i + 1, j)
            ]

    def mark_cell_visited(self, i, j):
        self.visited[i][j] = True

    def visited_cell(self, i, j):
        return self.visited[i][j]

    def is_valid_cell(self, i, j):
        return i in range(self.height) and j in range(self.width) and not (
            i == 0 or j == 0 or j == self.width - 1 or i == self.height - 1)

    def remove_the_wall_between_cells(self, i, j, neighbour_direction):
        neighbour_i, neighbour_j = -1, -1

        if neighbour_direction == Maze.NORTH:
            neighbour_i, neighbour_j = (i - 1, j)
        elif neighbour_direction == Maze.EAST:
            neighbour_i, neighbour_j = (i, j + 1)
        elif neighbour_direction == Maze.SOUTH:
            neighbour_i, neighbour_j = (i + 1, j)
        elif neighbour_direction == Maze.WEST:
            neighbour_i, neighbour_j = (i, j - 1)

        if self.is_a_wall_cell(neighbour_i, neighbour_j):
            self.grid[neighbour_i][neighbour_j] = Maze.EMPTY_CELL

    @staticmethod
    def get_cell_neighbours_and_directions(i, j):
        return [(i, j + 2, Maze.EAST), (i, j - 2, Maze.WEST), (i + 2, j, Maze.SOUTH), (i - 2, j, Maze.NORTH)]

    def distance_to_goal(self, i, j):
        return sqrt(abs(self.goal[0] - i) ** 2 + abs(self.goal[1] - j) ** 2)

    def is_a_wall_cell(self, neighbour_i, neighbour_j):
        return neighbour_i % 2 == 0 or neighbour_j % 2 == 0

    def get_cell_search_neighbours(self, i, j):
        return (
            (i, j + 1, self.grid[i][j + 1] == Maze.WALL_CELL),
            (i, j - 1, self.grid[i][j - 1] == Maze.WALL_CELL),
            (i - 1, j, self.grid[i - 1][j] == Maze.WALL_CELL),
            (i + 1, j, self.grid[i + 1][j] == Maze.WALL_CELL),
            # diagonal neighbors
            # (i + 1, j + 1, self.grid[i + 1][j + 1] == Maze.WALL_CELL),
            # (i - 1, j + 1, self.grid[i - 1][j + 1] == Maze.WALL_CELL),
            # (i + 1, j - 1, self.grid[i + 1][j - 1] == Maze.WALL_CELL),
            # (i - 1, j - 1, self.grid[i - 1][j - 1] == Maze.WALL_CELL)
        )

    def drop_all_walls(self):
        self.grid = self.__initiate_grid__(False)

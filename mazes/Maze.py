class Maze(object):
    # the cardinal directions and their inverses
    NORTH = 'n'
    EAST = 'e'
    SOUTH = 's'
    WEST = 'w'
    directions_inverses = {WEST: EAST, EAST: WEST, NORTH: SOUTH, SOUTH: NORTH}
    cardinal_directions = {NORTH, EAST, SOUTH, WEST}

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear_grid()
        self.walls = self.__construct_walls__()
        self.start = ()
        self.goal = ()
        self.start_picked = False
        self.visited = self.__visited_mappings__()

    def __initiate_grid__(self):
        return [[0 for _j in range(self.width)] for _i in range(self.height)]

    def __visited_mappings__(self):
        return {i: {j: False for j in range(self.width)} for i in range(self.height)}

    def __construct_walls__(self, with_walls=True):
        return {i: {j: {d: with_walls
                        for d in Maze.cardinal_directions
                        }
                    for j in range(self.width)
                    }
                for i in range(self.height)
                }

    def mark_all_cells_not_visited(self):
        self.visited = self.__visited_mappings__()

    def reconstruct_maze_grid(self):
        self.clear_grid()
        self.walls = self.__construct_walls__()
        self.visited = self.__visited_mappings__()

    def clear_grid(self):
        self.grid = self.__initiate_grid__()

    def clean_grid_mark_all_cells_not_visited(self):
        self.clear_grid()
        self.mark_all_cells_not_visited()

    def clear_all_walls(self, clear_walls=True):
        self.walls = self.__construct_walls__(not clear_walls)

    def get_cell_neighbours(self, i, j, with_walls=True):
        if with_walls:
            neighbors = [
                (i, j + 1, self.walls[i][j][Maze.EAST]),
                (i, j - 1, self.walls[i][j][Maze.WEST]),
                (i - 1, j, self.walls[i][j][Maze.NORTH]),
                (i + 1, j, self.walls[i][j][Maze.SOUTH])
            ]
        else:
            neighbors = [
                (i, j + 1),
                (i, j - 1),
                (i - 1, j),
                (i + 1, j)
            ]

        return neighbors

    def mark_cell_visited(self, i, j):
        self.visited[i][j] = True

    def visited_cell(self, i, j):
        return self.visited[i][j]

    def is_valid_cell(self, i, j):
        return i in range(self.height) and j in range(self.width)

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

        if self.is_valid_cell(neighbour_i, neighbour_j):
            self.walls[i][j][neighbour_direction] = False
            self.walls[neighbour_i][neighbour_j][Maze.directions_inverses[neighbour_direction]] = False
        pass

    @staticmethod
    def get_cell_neighbours_and_directions(i, j):
        return [(i, j + 1, Maze.EAST), (i, j - 1, Maze.WEST), (i + 1, j, Maze.SOUTH), (i - 1, j, Maze.NORTH)]
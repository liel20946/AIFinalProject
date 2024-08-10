# Example of how the self.variables looks like if the colors are (R, G, B,
#                                                                 Y) and the
# board is 4x4
# {
#     (0, 0): {'R': 1, 'G': 2, 'B': 3, 'Y': 4},
#     (0, 1): {'R': 5, 'G': 6, 'B': 7, 'Y': 8},
#     (0, 2): {'R': 9, 'G': 10, 'B': 11, 'Y': 12},
#     (0, 3): {'R': 13, 'G': 14, 'B': 15, 'Y': 16},
#
#     (1, 0): {'R': 17, 'G': 18, 'B': 19, 'Y': 20},
#     (1, 1): {'R': 21, 'G': 22, 'B': 23, 'Y': 24},
#     (1, 2): {'R': 25, 'G': 26, 'B': 27, 'Y': 28},
#     (1, 3): {'R': 29, 'G': 30, 'B': 31, 'Y': 32},
#
#     (2, 0): {'R': 33, 'G': 34, 'B': 35, 'Y': 36},
#     (2, 1): {'R': 37, 'G': 38, 'B': 39, 'Y': 40},
#     (2, 2): {'R': 41, 'G': 42, 'B': 43, 'Y': 44},
#     (2, 3): {'R': 45, 'G': 46, 'B': 47, 'Y': 48},
#
#     (3, 0): {'R': 49, 'G': 50, 'B': 51, 'Y': 52},
#     (3, 1): {'R': 53, 'G': 54, 'B': 55, 'Y': 56},
#     (3, 2): {'R': 57, 'G': 58, 'B': 59, 'Y': 60},
#     (3, 3): {'R': 61, 'G': 62, 'B': 63, 'Y': 64},
# }

import pycosat


class FlowFreeSAT:
    def __init__(self, board_size, colors, initial_board=None):
        self.board_size = board_size
        self.colors = colors
        self.num_colors = len(colors)
        self.variables = {}
        self.direction_variables = {}
        self.directions = {'─': [(0, -1), (0, 1)], '│': [(-1, 0), (1, 0)],
                           '┘': [(-1, 0), (0, -1)], '└': [(-1, 0), (0, 1)],
                           '┐': [(0, -1), (1, 0)], '┌': [(0, 1), (1, 0)]}
        self.reverse_directions = {'─': '│', '│': '─', '┘': '┌', '└': '┐',
                                   '┐': '└', '┌': '┘'}
        self.cnf = []
        self.initial_board = initial_board or {}

        # Initialize variables for each cell and color
        self.initialize_variables()
        # Add initial board constraints
        self.add_initial_board_constraints()

    def check_coords(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    # Example above
    def initialize_variables(self):
        var_id = 1
        for r in range(self.board_size):
            for c in range(self.board_size):
                self.variables[(r, c)] = {}
                for color in self.colors:
                    self.variables[(r, c)][color] = var_id
                    var_id += 1

        # Initialize variables for each cell and direction

        for r in range(self.board_size):
            for c in range(self.board_size):
                if (r, c) not in self.initial_board:
                    self.direction_variables[(r, c)] = {}
                    for direction in self.directions:
                        valid = True
                        for sub_directions in self.directions[direction]:
                            dr, dc = sub_directions
                            nr, nc = r + dr, c + dc
                            if not self.check_coords(nr, nc):
                                valid = False
                                break
                        if valid:
                            self.direction_variables[(r, c)][
                                direction] = var_id
                            var_id += 1

    # this method ensures that any cell with a predefined color in the initial board
    # is constrained to that color, and that no other colors are allowed in that cell.
    # For example for constraints for cell (1, 0) being 'R' will output :
    # [17], [-18], [-19], [-20]
    def add_initial_board_constraints(self):
        for (r, c), color in self.initial_board.items():
            for other_color in self.colors:
                if color == other_color:
                    self.cnf.append([self.variables[(r, c)][color]])
                else:
                    self.cnf.append([-self.variables[(r, c)][other_color]])

    # endpoint (a cell with a predefined color in the initial board) must be connected to
    # exactly one of its neighboring cells of the same color
    # assume : the cell (1, 0) with color 'R', it's neighbors and vaitables
    # id for 'R': (0, 0): 1, (2, 0): 33, (1, 1): 21
    # CNF Clauses
    # [
    #     [1, 33, 21],  # At least one neighbor is 'R'
    #     [-1, -33],
    #     # At most one neighbor is 'R' (not both (0, 0) and (2, 0) can be 'R')
    #     [-1, -21],
    #     # At most one neighbor is 'R' (not both (0, 0) and (1, 1) can be 'R')
    #     [-33, -21],
    #     # At most one neighbor is 'R' (not both (2, 0) and (1, 1) can be 'R')
    #     # Similar clauses would be added for other endpoints like (0, 3), (0, 0), (1, 3), etc.
    # ]

    def add_endpoint_constraints(self):
        for (r, c), color in self.initial_board.items():
            neighbors = self.get_neighbors(r, c)
            neighbor_vars = [self.variables[nr, nc][color] for nr, nc in
                             neighbors if (nr, nc) in self.variables]

            # Exactly one neighbor must match the cell's color
            self.cnf.append(neighbor_vars)  # At least one neighbor
            for i in range(len(neighbor_vars)):
                for j in range(i + 1, len(neighbor_vars)):
                    # Adding the clause to ensure no two neighbors can both have the same color
                    self.cnf.append([-neighbor_vars[i], -neighbor_vars[j]])

    # Every cell is assigned a single color.
    def add_single_color_constraints(self, variables):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if (
                        r,
                        c) not in self.initial_board:  # Only for non-endpoint cells
                    color_vars = [variables[(r, c)][color] for color in
                                  variables[(r, c)]]

                    # Each cell must have at least one color
                    self.cnf.append(color_vars)

                    # No cell can have more than one color
                    for i in range(len(color_vars)):
                        for j in range(i + 1, len(color_vars)):
                            self.cnf.append([-color_vars[i], -color_vars[j]])

    def add_direction_same_color_constraints(self):
        for dv in self.direction_variables:
            for direction in self.direction_variables[dv]:
                for sub_directions in self.directions[direction]:
                    x, y = dv[0] + sub_directions[0], dv[1] + sub_directions[1]
                    neighbor_coord = (x, y)
                    for color in self.variables[neighbor_coord]:
                        dv_color = self.variables[dv][color]
                        neighbor_color = self.variables[neighbor_coord][color]
                        self.cnf.append(
                            [-self.direction_variables[dv][direction],
                             -dv_color, neighbor_color])
                        self.cnf.append(
                            [-self.direction_variables[dv][direction],
                             dv_color, -neighbor_color])

    def completing_direction_neighbors_constraints(self):
        for dv in self.direction_variables:
            for direction in self.direction_variables[dv]:
                reverse_direction = self.reverse_directions[direction]
                for sub_directions in self.directions[reverse_direction]:
                    x, y = dv[0] + sub_directions[0], dv[1] + sub_directions[1]
                    neighbor_coord = (x, y)
                    if not self.check_coords(x, y):
                        continue
                    for color in self.variables[neighbor_coord]:
                        dv_color = self.variables[dv][color]
                        neighbor_color = self.variables[neighbor_coord][color]
                        self.cnf.append(
                            [-self.direction_variables[dv][direction],
                             -dv_color, -neighbor_color])

    def get_neighbors(self, r, c):
        neighbors = []
        if r > 0: neighbors.append((r - 1, c))  # Up
        if r < self.board_size - 1: neighbors.append((r + 1, c))  # Down
        if c > 0: neighbors.append((r, c - 1))  # Left
        if c < self.board_size - 1: neighbors.append((r, c + 1))  # Right
        return neighbors

    def solve(self):
        # Add constraints to CNF
        self.add_endpoint_constraints()
        self.add_single_color_constraints(self.variables)
        self.add_single_color_constraints(self.direction_variables)
        self.add_direction_same_color_constraints()
        self.completing_direction_neighbors_constraints()

        # Solve the SAT problem
        solution = pycosat.solve(self.cnf)
        return solution

    def print_board(self):
        board = [['.' for _ in range(self.board_size)] for _ in
                 range(self.board_size)]
        for (r, c), color in self.initial_board.items():
            board[r][c] = color
        for row in board:
            print(' '.join(row))

    def print_solution(self, solution):
        board = [['.' for _ in range(self.board_size)] for _ in
                 range(self.board_size)]

        for r in range(self.board_size):
            for c in range(self.board_size):
                for color in self.colors:
                    var = self.variables[(r, c)][color]
                    if var in solution:
                        board[r][c] = color

        print("\nSolution Board:")
        for row in board:
            print(' '.join(row))

    def convert_sol_to_board(self, solution):
        board = [['.' for _ in range(self.board_size)] for _ in
                 range(self.board_size)]

        for r in range(self.board_size):
            for c in range(self.board_size):
                for color in self.colors:
                    var = self.variables[(r, c)][color]
                    if var in solution:
                        board[r][c] = color
        return board

def is_path_connected(board, start_dot, end_dot):
    # Implement a basic DFS to check if there's a path from start to end
    visited = set()
    stack = [(start_dot.get_x(), start_dot.get_y())]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        x, y = stack.pop()
        if (x, y) == (end_dot.get_x(), end_dot.get_y()):
            return True
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and \
                        board[nx][ny] == start_dot.get_color():
                    stack.append((nx, ny))
    return False

def validate_sat_solution(sat_solution, dots_list):
    for i in range(0, len(dots_list), 2):
        start_dot = dots_list[i]
        end_dot = dots_list[i + 1]
        if not is_path_connected(sat_solution, start_dot, end_dot):
            return False
    return True

    # Example initial board setup
    # board_size = 4
    # colors = ['R', 'G', 'B', 'Y']
    # # Option 1
    # initial_board = {
    #     (0, 0): 'R',
    #     (0, 3): 'R',
    #     (1, 0): 'G',
    #     (1, 3): 'G',
    #     (2, 0): 'B',
    #     (2, 3): 'B',
    #     (3, 0): 'Y',
    #     (3, 3): 'Y'
    # }
    # # Option 2 - no solution
    # initial_board = {
    #     (1, 0): 'R',
    #     (0, 3): 'R',
    #     (0, 0): 'G',
    #     (1, 3): 'G',
    #     (2, 0): 'B',
    #     (2, 3): 'B',
    #     (3, 0): 'Y',
    #     (3, 3): 'Y'
    # }

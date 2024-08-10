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
import tkinter as tk
from gui import FlowFreeGUI


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

    # and '└' in
    # self.direction_variables[(r + 1, c)] and '┐' in \
    # self.direction_variables[(r, c + 1)] and '┘' in \
    # self.direction_variables[(r + 1, c + 1]):
    def add_square_preventing_constraints(self):
        for r in range(self.board_size - 1):
            for c in range(self.board_size - 1):
                if (
                        (r, c) in self.direction_variables and
                        (r + 1, c) in self.direction_variables and
                        (r, c + 1) in self.direction_variables and
                        (r + 1, c + 1) in self.direction_variables
                ):
                    if '┌' in self.direction_variables[(r, c)] and \
                            '└' in self.direction_variables[(r + 1, c)] and \
                            '┐' in self.direction_variables[(r, c + 1)] and \
                            '┘' in self.direction_variables[(r + 1, c + 1)]:
                        self.cnf.append([
                            -self.direction_variables[(r, c)]['┌'],
                            -self.direction_variables[(r + 1, c)]['└'],
                            -self.direction_variables[(r, c + 1)]['┐'],
                            -self.direction_variables[(r + 1, c + 1)]['┘']
                        ])

    def add_cycle_preventing_constraints(self, coordinates):
        cycle_cnf = []
        first = True
        for i in range(len(coordinates)):
            if i==0 and first:
                cycle_cnf.append(-self.direction_variables[coordinates[0][
                    0]]['┌'])
                first= False
            elif i == len(coordinates) - 1:
                cycle_cnf.append(
                    -self.direction_variables[coordinates[i][0]]['└'])
            else:
                cycle_cnf.append(
                    -self.direction_variables[coordinates[i][0]]['│'])
            if i == 0 or i == len(coordinates) - 1:
                action = '─'
            else:
                action = '│'
            for j in range(1, len(coordinates[i])-1):
                cycle_cnf.append(-self.direction_variables[coordinates[i][j]][action])

            if i == 0:
                cycle_cnf.append(-self.direction_variables[coordinates[i][
                    len(coordinates[i])-1]]['┐'])
            if i == len(coordinates) - 1:
                cycle_cnf.append(-self.direction_variables[coordinates[i][
                    len(coordinates[i])-1]]['┘'])

        self.cnf.append(cycle_cnf)


    def get_neighbors(self, r, c):
        neighbors = []
        if r > 0: neighbors.append((r - 1, c))  # Up
        if r < self.board_size - 1: neighbors.append((r + 1, c))  # Down
        if c > 0: neighbors.append((r, c - 1))  # Left
        if c < self.board_size - 1: neighbors.append((r, c + 1))  # Right
        return neighbors

    def solve(self, dots_list):
        # Add constraints to CNF
        self.add_endpoint_constraints()
        self.add_single_color_constraints(self.variables)
        self.add_single_color_constraints(self.direction_variables)
        self.add_direction_same_color_constraints()
        self.completing_direction_neighbors_constraints()
        # self.add_cycle_preventing_constraints()
        # Solve the SAT problem
        is_solution_without_cycle = False
        while(not is_solution_without_cycle):
            solution = pycosat.solve(self.cnf)
            if solution == "UNSAT":
                return solution
            solution_board = self.convert_sol_to_board(solution)
            is_solution_without_cycle, coordinates = analyze_solution(
                solution_board,
                dots_list)
            if coordinates:
                self.add_cycle_preventing_constraints(coordinates)
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

def group_by_row(coordinate_list):
    if not coordinate_list:
        return []

    grouped_rows = []
    current_row = []
    current_row_num = coordinate_list[0][
        0]  # Initialize with the row of the first element

    for coord in coordinate_list:
        x, y = coord
        if x == current_row_num:
            current_row.append((x, y))
        else:
            grouped_rows.append(current_row)
            current_row = [(x, y)]
            current_row_num = x

    if current_row:
        grouped_rows.append(current_row)

    return grouped_rows




def analyze_solution(board, dots_list):
    total_cells = len(board) * len(board[0])
    total_path_cells = 0
    visited = set()

    paths = []  # List to store paths

    # Find paths based on the dots_list
    for i in range(0, len(dots_list), 2):
        start_dot = dots_list[i]
        goal_dot = dots_list[i + 1]

        start_x, start_y = start_dot.get_x(), start_dot.get_y()
        goal_x, goal_y = goal_dot.get_x(), goal_dot.get_y()
        color = start_dot.get_color()

        path = find_path(board, start_x, start_y, color, visited)
        path_cells = path.size
        total_path_cells += path_cells
        paths.append(path)  # Add path to paths list

        last_node = path.get_last_node()
        # Check if the last node matches the goal
        # if last_node.x != goal_x or last_node.y != goal_y:
        #     print(f"Error: Path for color {color} does not end at the goal: {goal_x}, {goal_y}")
        #     print(f"Path ended at: {last_node.x}, {last_node.y} instead")

    leftovers = []
    # Identify leftover cells that are not part of any path
    for x in range(len(board)):
        for y in range(len(board[0])):
            if (x, y) not in visited and board[x][y] != "empty":
                leftovers.append((x, y))

    # Check if the board is fully filled
    unfilled_cells = total_cells - total_path_cells
    if unfilled_cells == 0:
        return True, None
    else:
        return False, group_by_row(leftovers)


def find_path(board, start_x, start_y, color, visited):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    path = LinkedList()
    x, y = start_x, start_y

    while True:
        path.append(x, y)
        visited.add((x, y))
        found_next = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and (
                    nx, ny) not in visited:
                if board[nx][ny] == color:
                    x, y = nx, ny
                    found_next = True
                    break

        if not found_next:
            break

    return path



class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
        self.tail = None

    def append(self, x, y):
        new_node = Node(x, y)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.tail = new_node
        self.size += 1

    def display(self):
        current = self.head
        path = []
        current_row = []
        current_row_num = current.x if current else None

        while current:
            if current.x == current_row_num:
                current_row.append((current.x, current.y))
            else:
                path.append(current_row)
                current_row = [(current.x, current.y)]
                current_row_num = current.x
            current = current.next

        if current_row:
            path.append(current_row)

        return path

    def get_last_node(self):
        return self.tail


import itertools
import pycosat
from functools import reduce

LEFT = 1
RIGHT = 2
TOP = 4
BOTTOM = 8

DELTAS = [(LEFT, 0, -1),
          (RIGHT, 0, 1),
          (TOP, -1, 0),
          (BOTTOM, 1, 0)]

DIR_TYPES = [LEFT | RIGHT, TOP | BOTTOM, TOP | LEFT, TOP | RIGHT,
             BOTTOM | LEFT, BOTTOM | RIGHT]
DIR_FLIP = {LEFT: RIGHT, RIGHT: LEFT, TOP: BOTTOM, BOTTOM: TOP}


class FlowFreeSolver:
    def __init__(self, size, colors, dots):
        self.size = size
        self.colors = colors
        self.dots = dots

    def color_var(self, i, j, color):
        return (i * self.size + j) * len(self.colors) + color + 1

    def make_color_clauses(self):
        clauses = []
        num_colors = len(self.colors)

        for i in range(self.size):
            for j in range(self.size):
                cell = self.dots[i][j]
                if cell in self.colors:
                    color_index = self.colors[cell]
                    clauses.append([self.color_var(i, j, color_index)])
                    for other_color in range(num_colors):
                        if other_color != color_index:
                            clauses.append(
                                [-self.color_var(i, j, other_color)])
                # else:
                #     clauses.append([self.color_var(i, j, color) for color in
                #                     range(num_colors)])
                    # clauses.extend(self.no_two(
                    #     [self.color_var(i, j, color) for color in
                    #      range(num_colors)]))

        return clauses

    def no_two(self, satvars):
        return ((-a, -b) for a, b in itertools.combinations(satvars, 2))

    def make_dir_vars(self):
        dir_vars = {}
        num_dir_vars = 0

        for i in range(self.size):
            for j in range(self.size):
                if self.dots[i][j] in self.colors:
                    continue

                cell_flags = reduce(lambda x, y: x | y, [bit for bit, ni, nj in
                                                         self.valid_neighbors(
                                                             i, j)], 0)
                dir_vars[(i, j)] = {code: num_dir_vars + 1 for code in
                                    DIR_TYPES if cell_flags & code == code}
                num_dir_vars += len(dir_vars[(i, j)])

        return dir_vars, num_dir_vars

    def valid_neighbors(self, i, j):
        return [(dir_bit, i + delta_i, j + delta_j) for
                dir_bit, delta_i, delta_j in DELTAS if
                0 <= i + delta_i < self.size and 0 <= j + delta_j < self.size]

    def make_dir_clauses(self, color_var, dir_vars):
        dir_clauses = []

        for i in range(self.size):
            for j in range(self.size):
                if self.dots[i][j] in self.colors:
                    continue

                cell_dir_vars = list(dir_vars.get((i, j), {}).values())
                if cell_dir_vars:
                    dir_clauses.append(cell_dir_vars)
                    dir_clauses.extend(self.no_two(cell_dir_vars))

                    for color in range(len(self.colors)):
                        color_1 = color_var(i, j, color)
                        for dir_bit, ni, nj in self.valid_neighbors(i, j):
                            color_2 = color_var(ni, nj, color)
                            for dir_type, dir_var in dir_vars.get((i, j),
                                                                  {}).items():
                                if dir_type & dir_bit:
                                    dir_clauses.append(
                                        [-dir_var, -color_1, color_2])
                                    dir_clauses.append(
                                        [-dir_var, color_1, -color_2])
                                elif 0 <= ni < self.size and 0 <= nj < self.size:
                                    dir_clauses.append(
                                        [-dir_var, -color_1, -color_2])

        return dir_clauses

    def solve(self):
        color_var = self.color_var
        color_clauses = self.make_color_clauses()
        # dir_vars, num_dir_vars = self.make_dir_vars()
        # dir_clauses = self.make_dir_clauses(color_var, dir_vars)
        #
        # num_vars = len(self.colors) * self.size ** 2 + num_dir_vars
        # clauses = color_clauses + dir_clauses
        clauses = color_clauses

        solution = pycosat.solve(clauses)
        if solution == 'UNSAT':
            return 'UNSAT'

        return solution

    def decode_solution(self, sol):
        num_colors = len(self.colors)
        decoded = [['' for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                cell_color = -1
                for color in range(num_colors):
                    if self.color_var(i, j, color) in sol:
                        cell_color = color
                decoded[i][j] = cell_color

        return decoded

    def initialize_board(self):
        # Create an empty board
        board = [['' for _ in range(self.board_size)] for _ in
                 range(self.board_size)]

        # Place two dots for each color
        num_colors = len(self.colors)
        color_positions = {color: [] for color in self.colors}

        # Generate pairs of positions for each color
        positions = [(i, j) for i in range(self.board_size) for j in
                     range(self.board_size)]
        random.shuffle(positions)

        for color in self.colors:
            pos1 = positions.pop()
            pos2 = positions.pop()
            color_positions[color] = [pos1, pos2]

        # Place dots on the board
        for color, (pos1, pos2) in color_positions.items():
            board[pos1[0]][pos1[1]] = color
            board[pos2[0]][pos2[1]] = color

        return board

def display_board(self):
    for row in self.board:
        print(' '.join([cell if cell else '.' for cell in row]))

if __name__ == "__main__":
    # Example usage
    size = 5
    colors = {'R': 0, 'B': 1}
    dots = [
        ['R', '', 'R', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', 'B', '', '', 'B']
    ]

    solver = FlowFreeSolver(size, colors, dots)
    solution = solver.solve()

    if solution == 'UNSAT':
        print("The puzzle is unsolvable.")
    else:
        decoded = solver.decode_solution(solution)
        for row in decoded:
            print(' '.join(str(c) for c in row))

from copy import deepcopy
from flow_game.move import Move

EMPTY_CELL = "black"


class Board:
    def __init__(self, board_size, dots_list):
        self.board_size = board_size
        self.dots_list = dots_list
        self.end_dots = {dot.get_color(): dot for dot in dots_list if
                         dot.get_is_goal()}
        self.paths = self.initialize_paths()
        self.game_board = self.initialize_board()

    def initialize_paths(self):
        paths = {}
        for dot in self.dots_list:
            if not dot.get_is_goal():
                paths[dot.get_color()] = (dot.get_x(), dot.get_y())
        return paths

    def initialize_board(self):
        board = [[EMPTY_CELL for i in range(self.board_size)] for j in
                 range(self.board_size)]
        for dot in self.dots_list:
            board[dot.get_x()][dot.get_y()] = dot.get_color()
        return board

    def get_legal_moves(self):
        move_list = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for color in self.paths.keys():
            x, y = self.paths[color]
            for direction in directions:
                dx, dy = direction
                if self.is_coord_valid(x + dx, y + dy) and self.is_move_valid(
                        x + dx, y + dy, color):
                    move_list.append(Move(x + dx, y + dy, color))
        return move_list

    def is_coord_valid(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_move_valid(self, x, y, color):
        return self.game_board[x][y] == EMPTY_CELL or (x, y) == (
            self.end_dots[color].get_x(), self.end_dots[color].get_y())

    def __copy__(self):
        new_board = Board.__new__(Board)
        new_board.board_size = self.board_size
        new_board.dots_list = self.dots_list
        new_board.end_dots = self.end_dots
        new_board.paths = {color: (x, y) for color, (x, y) in
                           self.paths.items()}
        new_board.game_board = [row[:] for row in self.game_board]
        return new_board

    def do_move(self, move):
        new_board = self.__copy__()
        new_board.game_board[move.get_x()][move.get_y()] = move.get_color()
        end_dot = new_board.end_dots[move.get_color()]
        if (move.get_x(), move.get_y()) == (end_dot.get_x(), end_dot.get_y()):
            del new_board.paths[move.get_color()]
        else:
            new_board.paths[move.get_color()] = (move.get_x(), move.get_y())
        return new_board

    def is_goal_state(self):
        return len(self.paths) == 0

    def __eq__(self, other):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.game_board[i][j] != other.game_board[i][j]:
                    return False
        return True

    def __hash__(self):
        return hash(str(self.game_board))

    def __str__(self):
        out_str = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                out_str.append(self.game_board[row][col])
                out_str.append(' ')
            out_str.append('\n')
        return ''.join(out_str)

from flow_game.move import Move

EMPTY_CELL = "black"


class Board:
    """
    This class represents the game board. It contains the current state of the
    game, the current color, the remaining colors, the current cost, the
    number of empty cells and the end dots.
    """
    def __init__(self, board_size, dots_list):
        """
        Constructor for the board
        :param board_size: the size of the board
        :param dots_list: the list of the starting dots
        """
        self.board_size = board_size
        self.dots_list = dots_list
        self.end_dots = {dot.get_color(): dot for dot in dots_list if
                         dot.get_is_goal()}
        self.paths = self.initialize_paths()
        self.remaining_colors = list(self.paths.keys())
        self.current_color = None
        self.game_board = self.initialize_board()
        self.choose_next_color()
        self.current_cost = 0
        self.number_empty_cells = (self.board_size ** 2 - (len(self.dots_list)
                                                           // 2))

    def get_cost(self):
        """
        Get the current cost of the board
        :return: the current cost of the board
        """
        return self.current_cost

    def remove_color(self, color):
        """
        Remove a color from the board
        :param color: the color to remove
        """
        del self.paths[color]
        self.remaining_colors.remove(color)
        self.choose_next_color()

    def choose_next_color(self):
        """
        Choose the next color to play
        """
        # first prioritize colors that the current flow cell is adjacent to a
        # wall, then choose the color with the least possible moves
        adjacent_to_wall = []
        for color in self.remaining_colors:
            x, y = self.paths[color]
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for direction in directions:
                dx, dy = direction
                if not self.is_coord_valid(x + dx, y + dy):
                    adjacent_to_wall.append(color)
                    break
        next_colors_lst = adjacent_to_wall if adjacent_to_wall else self.remaining_colors

        next_color, min_moves = None, float('inf')
        for color in next_colors_lst:
            moves = self.get_number_of_moves_for_color(color)
            if moves < min_moves:
                min_moves = moves
                next_color = color
        self.current_color = next_color

    def get_number_of_moves_for_color(self, color):
        """
        Get the number of possible moves for a specific color
        :param color: the color to check
        :return: the number of possible moves for the color
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = self.paths[color]
        moves = 0
        for direction in directions:
            dx, dy = direction
            if self.is_coord_valid(x + dx, y + dy) and self.is_move_valid(
                    x + dx, y + dy, color):
                moves += 1
        return moves

    def get_end_dots(self):
        """
        Get the end dots of the board
        :return: the end dots of the board
        """
        return self.end_dots

    def initialize_paths(self):
        """
        initialize the paths of the board
        :return: the initialized paths of the board
        """
        paths = {}
        for dot in self.dots_list:
            if not dot.get_is_goal():
                paths[dot.get_color()] = (dot.get_x(), dot.get_y())
        return paths

    def initialize_board(self):
        """
        initialize the board with empty cells, and the start dots
        :return: the initialized board
        """
        board = [[EMPTY_CELL for _ in range(self.board_size)] for _ in
                 range(self.board_size)]
        for dot in self.dots_list:
            board[dot.get_x()][dot.get_y()] = dot.get_color()
        return board

    def end_point_valid_move(self, x, y, color):
        """"
        Check if the move is valid for the end point
        :param x: the x coordinate of move
        :param y: the y coordinate of the move
        :param color: the color of the end point
        :return: true if the move is valid for the end point, false otherwise
        """
        return self.game_board[x][y] == EMPTY_CELL or (x, y) == self.paths[
            color]

    def is_end_point_stranded(self, color):
        """
        Check if the end point is stranded (no possible moves)
        :param color: the color of the end point
        :return: true if the end point is stranded, false otherwise
        """
        x, y = self.end_dots[color].get_x(), self.end_dots[color].get_y()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            dx, dy = direction
            if self.is_coord_valid(x + dx,
                                   y + dy) and self.end_point_valid_move(
                x + dx, y + dy, color):
                return False
        return True

    def get_legal_move_for_specific_cell(self, coord):
        """
        Get the legal moves for a specific cell
        :param coord: the coordinate of the cell
        :return: the legal moves for the cell
        """
        move_list = []
        x, y = coord
        cell_color = self.game_board[x][y]
        if cell_color == EMPTY_CELL:
            return move_list
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for direction in directions:
            dx, dy = direction
            if self.is_coord_valid(x + dx, y + dy) and self.is_move_valid(
                    x + dx, y + dy, cell_color):
                move_list.append(
                    Move(x + dx, y + dy, cell_color))
        return move_list

    def check_stranded_colors(self):
        """
        Check if there are any stranded colors (colors that have a stranded
        cell)
        :return: true if there are stranded colors, false otherwise
        """
        for color in self.remaining_colors:
            moves_for_flow = self.get_legal_move_for_specific_cell(
                self.paths[color])
            end_point_stranded = self.is_end_point_stranded(color)
            if end_point_stranded or not moves_for_flow:
                return True
        return False

    def get_legal_moves(self):
        """
        Get the legal moves for the current color
        :return: legal moves for the current color
        """
        if (not self.current_color) or (self.check_stranded_colors()):
            return []
        return self.get_legal_move_for_specific_cell(
            self.paths[self.current_color])

    def is_coord_valid(self, x, y):
        """
        Check if the coordinate is valid
        :param x: x coordinate
        :param y: y coordinate
        :return: true if the coordinate is valid, false otherwise
        """
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_move_valid(self, x, y, color):
        """
        Check if the move is valid
        :param x: x coordinate of the move
        :param y: y coordinate of the move
        :param color: color of the move
        :return: true if the move is valid, false otherwise
        """
        return self.game_board[x][y] == EMPTY_CELL or (x, y) == (
            self.end_dots[color].get_x(), self.end_dots[color].get_y())

    def __copy__(self):
        """
        Copy constructor for the board
        :return: a copy of the board
        """
        new_board = Board.__new__(Board)
        new_board.board_size = self.board_size
        new_board.dots_list = self.dots_list
        new_board.end_dots = self.end_dots
        new_board.paths = {color: (x, y) for color, (x, y) in
                           self.paths.items()}
        new_board.remaining_colors = [color for color in self.remaining_colors]
        new_board.game_board = [row[:] for row in self.game_board]
        new_board.current_color = self.current_color
        new_board.current_cost = self.current_cost
        new_board.number_empty_cells = self.number_empty_cells
        return new_board

    def finished_move(self, move, end_dot):
        """
        Check if the move is a finishing move (connects the start and end dots)
        :param move: the move to check
        :param end_dot: the end of the move color
        :return: true if the move is a finishing move, false otherwise
        """
        return (move.get_x(), move.get_y()) == (end_dot.get_x(),
                                                end_dot.get_y())

    def is_forced_move(self, move):
        """
        Check if the move is a forced move (only one possible move)
        :param move: the move to check
        :return: true if the move is a forced move, false otherwise
        """
        return (len(self.get_legal_moves()) == 1 and self.get_legal_moves()[
            0] == move)

    def do_move(self, move):
        """
        make a move on the board, return a new board with the updated state
        after the move
        :param move: the move to make
        :return: a new board with the updated state after the move
        """
        new_board = self.__copy__()
        new_board.game_board[move.get_x()][move.get_y()] = move.get_color()
        new_board.number_empty_cells -= 1
        end_dot = new_board.end_dots[move.get_color()]
        added_cost = 1
        if self.finished_move(move, end_dot):
            new_board.remove_color(move.get_color())
            added_cost = 0
        else:
            new_board.paths[move.get_color()] = (move.get_x(), move.get_y())
        if self.is_forced_move(move):
            added_cost = 0
        new_board.current_cost += added_cost
        return new_board

    def is_goal_state(self):
        """
        Check if the board is in a goal state
        :return: true if the board is in a goal state, false otherwise
        """
        return len(self.remaining_colors) == 0 and self.number_empty_cells == 0

    def __eq__(self, other):
        """
        Check if two boards are equal - have the same state and remaining colors
        :param other: the other board to compare
        :return: true if the boards are equal, false otherwise
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.game_board[i][j] != other.game_board[i][j]:
                    return False
        return self.remaining_colors == other.remaining_colors

    def __hash__(self):
        """
        Hash the board by hashing the game board and the remaining colors
        :return: the hash of the board
        """
        return hash((str(self.game_board), str(self.remaining_colors)))

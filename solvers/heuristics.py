EMPTY_CELL = "black"

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def get_manhattan_distance(board):
    manhattan_distance = 0
    for color, (x, y) in board.paths.items():
        end_dot = board.end_dots[color]
        goal_x, goal_y = end_dot.get_x(), end_dot.get_y()
        manhattan_distance += abs(x - goal_x) + abs(y - goal_y)
    return manhattan_distance


def combined_heuristic(board):
    manhattan_distance = get_manhattan_distance(board)
    return (manhattan_distance + count_empty_cells(board) + board.get_cost() +
            len(board.remaining_colors) + 2 * count_dead_cells(board) +
            2 * count_bad_cells(board))


def is_all_directions_are_blocked(i,j,board):
    for direction in directions:
        dx, dy = direction
        if board.is_coord_valid(i + dx, j + dy) and \
                board.game_board[i + dx][j + dy] == EMPTY_CELL:
            return False
    return True


def count_dead_cells(board):
    number_of_dead_cells = 0
    for i in range(board.board_size):
        for j in range(board.board_size):
            if board.game_board[i][j] == EMPTY_CELL:
                dead_end = is_all_directions_are_blocked(i,j,board)
                if dead_end:
                    number_of_dead_cells += 1
    return number_of_dead_cells


def count_empty_cells(board):
    number_of_empty_cells = 0
    for i in range(board.board_size):
        for j in range(board.board_size):
            if board.game_board[i][j] == EMPTY_CELL:
                number_of_empty_cells += 1
    return number_of_empty_cells


def count_same_color_neighbor(i,j, color, board):
    count = 0
    for direction in directions:
        dx, dy = direction
        if board.is_coord_valid(i + dx, j + dy) and \
                board.game_board[i + dx][j + dy] == color:
            count += 1
    return count


# a bad cell is a colord cell in which it has more than 2 neighbors of
# its own color. this is a bad cell because it will block the path
def count_bad_cells(board):
    bad_cells = 0
    for i in range(board.board_size):
        for j in range(board.board_size):
            if board.game_board[i][j] != EMPTY_CELL:
                color = board.game_board[i][j]
                num_of_same_color_neighbor = count_same_color_neighbor(i,j, color, board)
                if num_of_same_color_neighbor > 2:
                    bad_cells += 1
    return bad_cells


def simple_effective_heuristic(board):
    return board.get_cost() + count_empty_cells(board)

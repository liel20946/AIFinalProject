EMPTY_CELL = "black"


def combined_heuristic(board):
    manhattan_distance = 0
    for color, (x, y) in board.paths.items():
        end_dot = board.end_dots[color]
        goal_x, goal_y = end_dot.get_x(), end_dot.get_y()
        # Manhattan distance
        manhattan_distance += abs(x - goal_x) + abs(y - goal_y)

    return (manhattan_distance + count_empty_cells(board) + board.get_cost() +
            len(board.remaining_colors))


def count_empty_cells(board):
    number_of_empty_cells = 0
    for i in range(board.board_size):
        for j in range(board.board_size):
            if board.game_board[i][j] == EMPTY_CELL:
                number_of_empty_cells += 1
    return number_of_empty_cells


def simple_effective_heuristic(board):
    return board.get_cost() + count_empty_cells(board)

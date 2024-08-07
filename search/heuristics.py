EMPTY_CELL = "black"


def combined_heuristic(board):
    total_distance = 0
    for color, (x, y) in board.paths.items():
        end_dot = board.end_dots[color]
        goal_x, goal_y = end_dot.get_x(), end_dot.get_y()

        # Manhattan distance
        manhattan_distance = abs(x - goal_x) + abs(y - goal_y)

        # Blocked paths count
        blocked_paths = count_blocked_paths(board, (x, y), (goal_x, goal_y))

        # Combined heuristic
        total_distance += manhattan_distance + blocked_paths

    return total_distance


def count_blocked_paths(board, start, goal):
    x, y = start
    goal_x, goal_y = goal
    blocked = 0

    if x != goal_x:
        step = 1 if goal_x > x else -1
        for i in range(x + step, goal_x + step, step):
            if board.game_board[i][y] != EMPTY_CELL and board.game_board[i][
                y] != board.game_board[goal_x][goal_y]:
                blocked += 1

    if y != goal_y:
        step = 1 if goal_y > y else -1
        for j in range(y + step, goal_y + step, step):
            if board.game_board[x][j] != EMPTY_CELL and board.game_board[x][
                j] != board.game_board[goal_x][goal_y]:
                blocked += 1

    return blocked

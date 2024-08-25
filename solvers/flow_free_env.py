def is_dot_free(state, dot):
    """
    Check if the given dot is free in the given state
    :param state: the state to check
    :param dot: the dot to check
    :return: whether the dot is free
    """
    x, y = state.paths[dot]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        dx, dy = direction
        if state.is_coord_valid(x + dx, y + dy) and \
                state.game_board[x + dx][y + dy] == "black":
            return True
    return False


def check_dead_ends(state):
    """
    Check the number of dead ends in the given state
    :param state: the state to check
    :return: number of dead ends
    """
    num_of_dead_ends = 0
    for dot in state.paths:
        if not is_dot_free(state, dot):
            num_of_dead_ends += 1
    return num_of_dead_ends


class FlowFreeEnvironment:
    """
    This class wraps the FlowFreeProblem class to be used as an environment for
    reinforcement learning.
    """
    def __init__(self, problem):
        """
        Constructor for the FlowFreeEnvironment class.
        :param problem: the problem to solve
        """
        self.initial_state = problem.get_start_state()
        self.state = self.initial_state

    def reset(self):
        """
        Resets the environment to its initial state.
        :return: the initial state
        """
        self.state = self.initial_state
        return self.state

    def step(self, action):
        """
        Applies the given action to the environment.
        :param action: the action to apply
        :return: the new state, reward and whether the episode is done
        """
        # Apply action to the board and get the new state and reward
        is_curr_finished = self.state.is_goal_state()
        self.state = self.state.do_move(action)
        no_moves = len(self.state.get_legal_moves()) == 0  # Done if no more
        finished_board = self.state.is_goal_state()  # Done if all paths are connected

        # reward function
        total_number_of_pairs = len(self.state.dots_list) // 2
        # moves
        reward = 0
        if is_curr_finished:
            reward = 500
        elif finished_board:
            reward = 1000
        elif no_moves:
            reward = -1000
        elif action.get_color() not in self.state.remaining_colors:
            reward = 50 * (total_number_of_pairs - len(self.state.paths)) / total_number_of_pairs
        elif action.get_color() not in [move.get_color() for move in self.state.get_legal_moves()]:
            reward = -200
        return self.state, reward, no_moves

    def set_state(self, state):
        self.state = state

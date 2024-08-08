class FlowFreeEnvironment:
    def __init__(self, problem):
        self.initial_state = problem.get_start_state()
        self.state = self.initial_state

    def get_colors(self):
        return list(set([dot.get_color() for dot in self.state.dots_list]))

    def reset(self):
        self.state = self.initial_state
        return self.state

    def check_dead_ends(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        num_of_dead_ends = 0
        for dot in self.state.paths:
            x, y = self.state.paths[dot]
            dead_end = True
            for direction in directions:
                dx, dy = direction
                if self.state.is_coord_valid(x + dx, y + dy) and self.state.game_board[x + dx][y + dy] == "black":
                    dead_end = False
                    break
            if dead_end:
                num_of_dead_ends += 1
        return num_of_dead_ends

    def step(self, action):
        # Apply action to the board and get the new state and reward
        pre_path_num = len(self.state.paths)
        self.state = self.state.do_move(action)
        no_moves = len(self.state.get_legal_moves()) == 0  # Done if no more
        finished_board = self.state.is_goal_state()  # Done if all paths are connected

        #reward function
        total_number_of_pairs = len(self.state.dots_list) // 2
        # moves
        reward = -self.check_dead_ends() * (100 / total_number_of_pairs)
        if finished_board:
            reward = 100
        elif pre_path_num > len(self.state.paths):
            reward += (total_number_of_pairs - len(self.state.paths)) * (100 /
                                                                        total_number_of_pairs)
        elif no_moves and not finished_board:
            reward = -100
        return self.state, reward, no_moves

    def set_state(self, state):
        self.state = state

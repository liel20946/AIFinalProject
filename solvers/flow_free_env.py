class FlowFreeEnvironment:
    def __init__(self, problem):
        self.initial_state = problem.get_start_state()
        self.state = self.initial_state

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
                if self.state.is_coord_valid(x + dx, y + dy) and \
                        self.state.game_board[x + dx][y + dy] == "black":
                    dead_end = False
                    break
            if dead_end:
                num_of_dead_ends += 1
        return num_of_dead_ends
    
    def reward_direction(self, action):
        # Apply action to the board and get the new state and reward
        pre_path_num = len(self.state.paths)
        # x, y = self.state.paths[self.state.get_color_lst()[-1]]
        no_moves = len(self.state.get_legal_moves()) == 0  # Done if no more
        finished_board = self.state.is_goal_state()  # Done if all paths are connected
        # reward = 0
        # end_dot = self.state.get_end_dots()[self.state.get_color_lst()[-1]]
        # x_end_point, y_end_point = end_dot.get_x(), end_dot.get_y()
        #
        # if x_end_point<x:
        #     if not(action.get_x()== x+1 and action.get_y() == y):  down
        #         reward -= 30
        # if x_end_point>x:
        #     if not(action.get_x()== x-1 and action.get_y() == y): #not up
        #         reward -= 30
        #
        # if x==0 or x==len(self.state.game_board)-1:
        #     if y_end_point<y:
        #         if not(action.get_x()== x and action.get_y() == y-1): #not left
        #             reward -= 30
        #     if y_end_point>y:
        #         if not(action.get_x()== x and action.get_y() == y+1): #not
        #             # right
        #             reward -= 30
        # return self.state, reward, no_moves

    def step(self, action):
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
        elif action.get_color() not in self.state.color_lst:
            reward = 50 * (total_number_of_pairs - len(self.state.paths)) / total_number_of_pairs
        elif action.get_color() not in [move.get_color() for move in self.state.get_legal_moves()]:
            reward = -200
        # check for dead ends
        # elif self.check_dead_ends() > 0:
        #     reward = -100
        # elif pre_path_num > len(self.state.paths):
        #     reward += (total_number_of_pairs - len(self.state.paths)) * (100 /
        #                                                                  total_number_of_pairs)
        return self.state, reward, no_moves

    def set_state(self, state):
        self.state = state

import random
import numpy as np


class ApproxQLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability
        self.weights = np.zeros(4)  # Initialize weights for three features

    def get_features(self, state, action):
        # Calculate features for the given state-action pair
        next_state = state.do_move(action)
        num_completed_paths = len(state.dots_list) // 2 - len(next_state.paths)
        num_legal_moves = len(next_state.get_legal_moves())
        num_dead_ends = self.check_dead_ends(next_state)
        manhattan_distance = sum(
            [abs(corr[0] - next_state.end_dots[color].get_x()) +
             abs(corr[1] - next_state.end_dots[color].get_y()) for color, corr
             in next_state.paths.items()])  # Manhattan  distance

        features = np.array([num_completed_paths, num_legal_moves,
                             -num_dead_ends, -manhattan_distance])
        return features / 1000

    def check_dead_ends(self, state):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        num_of_dead_ends = 0
        for dot in state.paths:
            x, y = state.paths[dot]
            dead_end = True
            for direction in directions:
                dx, dy = direction
                if state.is_coord_valid(x + dx, y + dy) and \
                        state.game_board[x + dx][y + dy] == "black":
                    dead_end = False
                    break
            if dead_end:
                num_of_dead_ends += 1
        return num_of_dead_ends

    def get_q_value(self, state, action):
        features = self.get_features(state, action)
        res = np.dot(self.weights, features)
        return res

    def update_weights(self, state, action, reward, next_state):
        features = self.get_features(state, action)
        if len(next_state.get_legal_moves()) == 0:
            td_target = reward
        else:
            next_q_values = [self.get_q_value(next_state, next_action) for
                             next_action in next_state.get_legal_moves()]
            td_target = reward + self.gamma * max(next_q_values)
        td_error = td_target - self.get_q_value(state, action)
        self.weights += self.alpha * td_error * features

    def get_best_action(self, state):
        valid_actions = self.get_next_actions(state)
        if len(valid_actions) == 0:
            return None, True
        q_values = [self.get_q_value(state, action) for action in
                    valid_actions]
        max_q_value = max(q_values)
        best_actions = [action for action, q_value in
                        zip(valid_actions, q_values) if q_value == max_q_value]
        return random.choice(best_actions), False

    def get_next_actions(self, state):
        color_moves = state.get_legal_moves()
        if len(color_moves) == 0:
            return []
        return color_moves

    def choose_action(self, state):
        next_actions = state.get_legal_moves()
        # next_actions = self.get_next_actions(state)
        if len(next_actions) > 0:
            return random.choice(next_actions), False
        else:
            return None, True
        # if random.uniform(0, 1) < self.epsilon:
        #     return random.choice(state.get_legal_moves())
        # else:
        #     return self.get_best_action(state)

    def blocked_state(self, state):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dot in state.paths:
            x, y = state.paths[dot]
            dead_end = True
            for direction in directions:
                dx, dy = direction
                if state.is_coord_valid(x + dx, y + dy) and \
                        state.game_board[x + dx][y + dy] == "black":
                    dead_end = False
                    break
            if dead_end:
                return True
        return False

    def train(self, episodes, environment):
        for episode in range(episodes):
            print(f"Episode {episode + 1}")
            state = environment.reset()
            done = False
            while not done:
                action, skip = self.choose_action(state)
                if skip:
                    break
                next_state, reward, done = environment.step(action)
                self.update_weights(state, action, reward, next_state)
                state = next_state
                if self.blocked_state(state):
                    done = True

    def solve(self, state, environment):
        actions = []
        done = False
        while not done:
            action, stop = self.get_best_action(state)
            if stop:
                break
            actions.append(action)
            state, _, done = environment.step(action)
        return actions

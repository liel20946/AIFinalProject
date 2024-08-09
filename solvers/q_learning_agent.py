import random


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.9):
        self.q_table = {}  # Q-table for storing state-action values
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        if len(next_state.get_legal_moves()) == 0:
            td_target = reward
        else:
            best_next_action = self.get_best_action(next_state)
            td_target = reward + self.gamma * self.get_q_value(next_state,
                                                               best_next_action)
        td_error = td_target - self.get_q_value(state, action)
        new_q_value = self.get_q_value(state, action) + self.alpha * td_error
        self.q_table[(state, action)] = new_q_value

    def get_best_action(self, state):
        valid_actions = state.get_legal_moves()
        q_values = [self.get_q_value(state, action) for action in
                    valid_actions]
        max_q_value = max(q_values)
        best_actions = [action for action, q_value in
                        zip(valid_actions, q_values) if q_value == max_q_value]
        return random.choice(best_actions)

    def choose_action(self, state):
        # return random.choice(state.get_legal_moves())
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(state.get_legal_moves())
        else:
            return self.get_best_action(state)

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
        win_counter = 0
        for episode in range(episodes):
            print(f"Episode {episode + 1}")
            state = environment.reset()
            done = False
            while not done:
                action = self.choose_action(state)
                next_state, reward, done = environment.step(action)
                self.update_q_value(state, action, reward, next_state)
                state = next_state
                if self.blocked_state(state):
                    done = True
            if state.is_goal_state():
                win_counter += 1
                print("won")

    def solve(self, state, environment):
        actions = []
        done = False
        while not done:
            action = self.get_best_action(state)
            actions.append(action)
            state, _, done = environment.step(action)
        return actions

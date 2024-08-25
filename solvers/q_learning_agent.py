import random
from solvers.flow_free_env import check_dead_ends


class QLearningAgent:
    """
    Q-learning agent for solving the game.
    """
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.9):
        """
        Constructor for the QLearningAgent class.
        :param alpha: alpha parameter for the agent
        :param gamma: gamma parameter for the agent
        :param epsilon: epsilon parameter for the agent
        """
        self.q_table = {}  # Q-table for storing state-action values
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability

    def get_q_value(self, state, action):
        """
        Get the Q value for the given state-action pair.
        :param state: state to get Q value for
        :param action: action to get Q value for
        :return: Q value for the state-action pair
        """
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        """
        Update the Q value for the given state-action pair.
        :param state: state to update Q value for
        :param action: action to update Q value for
        :param reward: reward received
        :param next_state: next state
        """
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
        """
        Get the best action for the given state.
        :param state: state to get the best action for
        :return: best action for the state
        """
        valid_actions = state.get_legal_moves()
        q_values = [self.get_q_value(state, action) for action in
                    valid_actions]
        max_q_value = max(q_values)
        best_actions = [action for action, q_value in
                        zip(valid_actions, q_values) if q_value == max_q_value]
        return random.choice(best_actions)

    def choose_action(self, state):
        """
        Choose an action for the given state.
        :param state: state to choose action for
        :return: chosen action
        """
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(state.get_legal_moves())
        else:
            return self.get_best_action(state)

    def train(self, episodes, environment):
        """
        Train the agent for the given number of episodes.
        :param episodes: number of episodes to train for
        :param environment: environment to train on
        :return: number of wins
        """
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
                if check_dead_ends(state) > 0:
                    done = True
            if state.is_goal_state():
                win_counter += 1
                print("won")

    def solve(self, state, environment):
        """
        Solve the game using the trained agent.
        :param state: state to solve
        :param environment: environment to solve in
        :return: list of actions to solve the game
        """
        actions = []
        done = False
        while not done:
            action = self.get_best_action(state)
            actions.append(action)
            state, _, done = environment.step(action)
        return actions

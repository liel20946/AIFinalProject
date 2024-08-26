import random
import numpy as np
from solvers.flow_free_env import check_dead_ends


class ApproxQLearningAgent:
    """
    Approximate Q-learning agent for the Flow Free game
    """

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        Constructor for the ApproxQLearningAgent class.
        :param alpha: alpha parameter for the agent
        :param gamma: gamma parameter for the agent
        :param epsilon: epsilon parameter for the agent
        """
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability
        self.weights = np.zeros(4)  # Initialize weights for three features

    def get_features(self, state, action):
        """
        Calculate features for the given state-action pair
        :param state: state to calculate features for
        :param action: action to calculate features for
        :return: value of the features
        """
        next_state = state.do_move(action)
        num_completed_paths = len(state.dots_list) // 2 - len(next_state.paths)
        num_legal_moves = len(next_state.get_legal_moves())
        num_dead_ends = check_dead_ends(next_state)
        manhattan_distance = sum(
            [abs(corr[0] - next_state.end_dots[color].get_x()) +
             abs(corr[1] - next_state.end_dots[color].get_y()) for color, corr
             in next_state.paths.items()])  # Manhattan  distance
        features = np.array([num_completed_paths, num_legal_moves,
                             -num_dead_ends, -manhattan_distance])
        return features / 1000

    def get_q_value(self, state, action):
        """
        get the Q value for the given state-action pair
        :param state: state to get Q value for
        :param action: action to get Q value for
        :return: Q value for the state-action pair
        """
        features = self.get_features(state, action)
        res = np.dot(self.weights, features)
        return res

    def update_weights(self, state, action, reward, next_state):
        """
        Update the weights of the agent.
        :param state: current state
        :param action: action taken
        :param reward: reward received
        :param next_state: next state
        """
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
        """
        Get the best action for the given state.
        :param state: state to get best action for
        :return: best action for the state
        """
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
        """
        Get the possible next actions for the given state.
        :param state: state to get next actions for
        :return: possible next actions for the state
        """
        color_moves = state.get_legal_moves()
        if len(color_moves) == 0:
            return []
        return color_moves

    def choose_action(self, state):
        """
        Choose an action for the given state.
        :param state: state to choose action for
        :return: chosen action for the state
        """
        next_actions = state.get_legal_moves()
        if len(next_actions) > 0:
            return random.choice(next_actions), False
        else:
            return None, True

    def train(self, episodes, environment):
        """
        Train the agent on the given environment.
        :param episodes: number of episodes to train for
        :param environment: environment to train on
        """
        for episode in range(episodes):
            state = environment.reset()
            done = False
            while not done:
                action, skip = self.choose_action(state)
                if skip:
                    break
                next_state, reward, done = environment.step(action)
                self.update_weights(state, action, reward, next_state)
                state = next_state
                if check_dead_ends(state) > 0:
                    done = True

    def solve(self, state, environment):
        """
        Solve the given state using the agent.
        :param state: state to solve
        :param environment: environment to solve in
        :return: actions to solve the state
        """
        actions = []
        done = False
        while not done:
            action, stop = self.get_best_action(state)
            if stop:
                break
            actions.append(action)
            state, _, done = environment.step(action)
        return actions

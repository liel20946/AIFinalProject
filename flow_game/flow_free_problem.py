from flow_game.board import Board


class FlowFreeProblem:
    """
    A class to represent the problem of solving a Flow Free
    puzzle. This class is used by the solvers.
    """

    def __init__(self, board_size, dots_list):
        """
        Constructor for the FlowFreeProblem class.
        :param board_size: size of the board
        :param dots_list: list of the start dots on the board
        """
        self.board = Board(board_size, dots_list)
        self.expanded = 0
        self.board_size = board_size
        self.dots_list = dots_list

    def get_problem_vars(self):
        """
        Getter for the problem variables.
        :return: board size and list of dots
        """
        return self.board_size, self.dots_list

    def get_start_state(self):
        """
        Getter for the start state of the problem.
        :return: start state of the problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        Returns whether the given state is a goal state.
        this is an overlay method for the state's is_goal_state method.
        :param state: state to check
        :return: whether the state is a goal state
        """
        return state.is_goal_state()

    def get_successors(self, state):
        """
        Returns the successors of the given state.
        :param state: state to get successors from
        :return: list of successors
        """
        self.expanded = self.expanded + 1
        return [(state.do_move(move), move, 1) for move in (
            state.get_legal_moves())]

    def get_cost_of_actions(self, actions):
        """
        Returns the cost of the given actions.
        :param actions: actions to get cost of
        :return: cost of the actions, in this case the length of the actions
        """
        return len(actions)

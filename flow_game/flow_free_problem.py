from flow_game.board import Board


class FlowFreeProblem:
    """
    A one-player Blokus game as a solvers problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_size, dots_list):
        self.board = Board(board_size, dots_list)
        self.expanded = 0
        self.board_size = board_size
        self.dots_list = dots_list

    def get_problem_vars(self):
        return self.board_size, self.dots_list

    def get_start_state(self):
        """
        Returns the start state for the solvers problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return state.is_goal_state()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the solvers problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(move), move, 1) for move in (
            state.get_legal_moves())]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

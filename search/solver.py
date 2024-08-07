from search import util


# DFS
def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    return general_search(problem, util.Stack())


# BFS
def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return general_search(problem, util.Queue())


def general_search(problem, fringe):
    """
    general search algorithm, takes a problem and a fringe and returns a list of actions that reaches.
    """
    visited = set()
    fringe.push((problem.get_start_state(), []))
    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if problem.is_goal_state(state):
            return actions
        if state not in visited:
            visited.add(state)
            for successor, action, step_cost in problem.get_successors(state):
                if successor not in visited:
                    fringe.push((successor, actions + [action]))
    return []


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push(Pair(problem.get_start_state(), []), 0)
    while not fringe.isEmpty():
        state, actions = fringe.pop().unpack()
        if problem.is_goal_state(state):
            return actions
        if state not in visited:
            visited.add(state)
            for successor, action, step_cost in problem.get_successors(state):
                if successor not in visited:
                    fringe.push(Pair(successor, actions + [action]),
                                problem.get_cost_of_actions(
                                    actions + [action]))
    return []


def null_heuristic(state):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    visited = set()
    fringe.push(Pair(problem.get_start_state(), []), 0)
    while not fringe.isEmpty():
        state, actions = fringe.pop().unpack()
        if problem.is_goal_state(state):
            return actions
        if state not in visited:
            visited.add(state)
            for successor, action, step_cost in problem.get_successors(state):
                if successor not in visited:
                    cost = problem.get_cost_of_actions(
                        actions + [action]) + heuristic(successor)
                    fringe.push(Pair(successor, actions + [action]), cost)
    return []

    # class for the search algorithms


class Pair:
    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

    def unpack(self):
        return self.state, self.actions

    # Abbreviations


bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search

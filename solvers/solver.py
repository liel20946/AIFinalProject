from solvers.util import Stack
from solvers.util import Queue
from solvers.util import PriorityQueue
from solvers.util import Pair


# DFS
def depth_first_search(problem):
    """
    run the depth first search algorithm on the given problem.
    :param problem: the problem to solve.
    :return: a list of actions that reaches the goal state.
    """
    return general_search(problem, Stack())


# BFS
def breadth_first_search(problem):
    """
    run the breadth first search algorithm on the given problem.
    :param problem: the problem to solve.
    :return: a list of actions that reaches the goal state.
    """
    return general_search(problem, Queue())


def general_search(problem, fringe):
    """
    General search algorithm.
    :param problem: the problem to solve.
    :param fringe: the data structure to use for the search.
    :return: a list of actions that reaches the goal state.
    """
    visited = set()
    fringe.push((problem.get_start_state(), []))
    while not fringe.is_empty():
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
    run the uniform cost search algorithm on the given problem.
    :param problem: the problem to solve.
    :return: a list of actions that reaches the goal state.
    """
    fringe = PriorityQueue()
    visited = set()
    fringe.push(Pair(problem.get_start_state(), []), 0)
    while not fringe.is_empty():
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
    A null heuristic function.
    :param state: the state to evaluate.
    :return: 0
    """
    return 0

# A* search
def a_star_search(problem, heuristic=null_heuristic):
    """
    run the A* search algorithm on the given problem.
    :param problem: the problem to solve.
    :param heuristic: the heuristic function to use.
    :return: a list of actions that reaches the goal state.
    """
    fringe = PriorityQueue()
    visited = set()
    fringe.push(Pair(problem.get_start_state(), []), 0)
    while not fringe.is_empty():
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





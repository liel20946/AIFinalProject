from flow_game.flow_free_problem import FlowFreeProblem
from main import run_search_algorithm
from main import convert_dots_to_sat_problem
from solvers.SAT import FlowFreeSAT
from main import choose_rl_agent
from problems.image_to_dots import convert_image_to_dots


import signal

from solvers.flow_free_env import FlowFreeEnvironment

PROBLEMS_DIR_NAME = "problems//levels_pngs"

SAT_FAILED = "UNSAT"
LINE_FORMAT_ERROR = "Unexpected line format"
NUMBER_OF_LEVELS_PER_GRID_SIZE = 10
MIN_GRID_SIZE = 5
MAX_GRID_SIZE = 14

class TimeoutException(Exception):
    """
    Class for a timeout exception.
    """
    pass

def timeout_handler(signum, frame):
    """
    Handle a timeout signal.
    :param signum: signal number
    :param frame: frame
    :return: None
    """
    raise TimeoutException()


# Set up the timeout handler
signal.signal(signal.SIGALRM, timeout_handler)


def run_with_timeout(timeout, function, *args, **kwargs):
    """
    Run a function with a timeout.
    :param timeout: timeout in seconds
    :param function: function to run
    :param args: arguments
    :param kwargs: keyword arguments
    :return: the result of the function or None if it times out
    """
    signal.alarm(timeout)  # Set the timeout in seconds
    try:
        result = function(*args, **kwargs)
    except TimeoutException:
        result = None
    finally:
        signal.alarm(0)  # Disable the alarm
    return result


def load_levels(grid_size):
    """
    Load the levels for the given grid size.
    :param grid_size: size of the grid
    :return: list of levels
    """
    # iterate over the files in problems directory,
    # use process_image to convert the image of the specific grid size to a
    # list of lists where each sublist represents a level
    loaded_levels = []
    for i in range(NUMBER_OF_LEVELS_PER_GRID_SIZE):
        level = convert_image_to_dots(f'{PROBLEMS_DIR_NAME}/'
                              f'{grid_size}x{grid_size}_{i+1}.png',
                                      grid_size)
        loaded_levels.append(level)

    return loaded_levels


def print_results(algorithm, problems_not_passed_lst,
                  num_of_passed_problems, levels):
    """
    Print the results of the algorithm.
    :param algorithm: name of the algorithm
    :param problems_not_passed_lst: list of problems not passed
    :param num_of_passed_problems: number of problems passed
    :param levels: list of levels
    :return:
    """
    print(f'{algorithm} passed {num_of_passed_problems}/{len(levels)}')
    if problems_not_passed_lst:
        print(f'problems not passed: {problems_not_passed_lst}')
    print('---------------------------------------------------')



def simulate_sat_solver(levels, grid_size):
    """
    Simulate the SAT solver on the given levels.
    :param levels: list of levels
    :param grid_size: size of the grid
    """
    num_of_passed_problems = 0
    problems_not_passed_lst = []
    for level_num, level in enumerate(levels):
        colors, initial_board = convert_dots_to_sat_problem(level)
        sat_solver = FlowFreeSAT(grid_size, colors, initial_board)
        solution = sat_solver.solve(level)
        if solution == SAT_FAILED:
            problems_not_passed_lst.append(level_num + 1)
            continue
        num_of_passed_problems += 1
    print_results("SAT", problems_not_passed_lst, num_of_passed_problems, levels)



def simulate_q_learning_solver(levels, grid_size):
    """
    Simulate the Q learning solver on the given levels.
    :param levels: list of levels
    :param grid_size: size of the grid
    """
    q_algorithms = ["Q learning", "AQ learning"]
    for algo in q_algorithms:
        problems_not_passed_lst = []
        problems_passed_counter = 0
        for level_num, level in enumerate(levels):
            problem = FlowFreeProblem(grid_size, level)
            environment = FlowFreeEnvironment(problem)
            agent = choose_rl_agent(algo)
            agent.train(episodes=5000, environment=environment)
            initial_state = environment.reset()
            actions = agent.solve(initial_state, environment)
            problem_state = problem.get_start_state()
            for action in actions:
                problem_state = problem_state.do_move(action)
            if problem_state.is_goal_state():
                problems_passed_counter += 1
            else:
                problems_not_passed_lst.append(level_num + 1)

        print_results(algo, problems_not_passed_lst, problems_passed_counter)


def solve_search_problem(algo, problem_dots, grid_size):
    """
    Solve the search problem using the given algorithm.
    :param algo: algorithm to use
    :param problem_dots: list of dots representing the problem
    :param grid_size: size of the grid
    :return: the goal state of the problem
    """
    problem = FlowFreeProblem(grid_size, problem_dots)
    actions = run_with_timeout(3, run_search_algorithm, algo, problem)
    problem_state = problem.get_start_state()
    if actions is None:
        return problem_state
    for action in actions:
        problem_state = problem_state.do_move(action)
    return problem_state


def simulate_search_algorithm(levels, grid_size):
    """
    Simulate the search algorithm on the given levels.
    :param levels: list of levels
    :param grid_size: size of the grid
    """
    search_algorithms = ["BFS", "DFS", "UCS", "A*"]
    results = {algo: 0 for algo in search_algorithms}
    for algo in search_algorithms:
        problems_not_passed_lst = []
        problems_passed_counter = 0
        for level_num, level in enumerate(levels):
            solution = solve_search_problem(algo, level, grid_size)
            if solution.is_goal_state():
                problems_passed_counter += 1
            else:
                problems_not_passed_lst.append(level_num + 1)
        results[algo] = problems_passed_counter

        print_results(algo, problems_not_passed_lst,
                      problems_passed_counter, levels)

solvers = {"Search": simulate_search_algorithm,
           "SAT": simulate_sat_solver, "Q learning":
               simulate_q_learning_solver}


def simulate_all(grid_size, levels):
    """
    Simulate all algorithms on the given levels.
    :param grid_size: size of the grid
    :param levels: list of levels
    """
    for solver_type in solvers.keys():
            solvers.get(solver_type)(levels, grid_size)

def simulate_algorithms_for_grid_size(algorithm_type, grid_size,levels):
    """
    Simulate the algorithms for the given grid size.
    :param algorithm_type: type of algorithm to simulate
    :param grid_size: size of the grid
    :param levels: list of levels
    """
    if algorithm_type == "All":
        simulate_all(grid_size,levels)
    else:
        solvers.get(algorithm_type)(levels, grid_size)

if __name__ == "__main__":
    for size in range(MIN_GRID_SIZE, MAX_GRID_SIZE + 1):
        print("Simulating algorithms for grid size:", size)
        levels = load_levels(size)
        algorithm_type = "SAT"
        simulate_algorithms_for_grid_size(algorithm_type, size, levels)
        print()




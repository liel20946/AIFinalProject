from flow_game.flow_free_problem import FlowFreeProblem
from main import run_search_algorithm
from flow_game.dot import Dot
from main import convert_dots_to_sat_problem
from solvers.SAT import FlowFreeSAT
from main import choose_rl_agent
from main import display_initial_board

import signal

from solvers.flow_free_env import FlowFreeEnvironment

PROBLEMS_DIR_NAME = "problems"
PROBLEM_FILE_PREFIX = "levels"
SAT_FAILED = "UNSAT"
LINE_FORMAT_ERROR = "Unexpected line format"
MIN_GRID_SIZE = 5
MAX_GRID_SIZE = 10

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()


# Set up the timeout handler
signal.signal(signal.SIGALRM, timeout_handler)


def run_with_timeout(timeout, function, *args, **kwargs):
    signal.alarm(timeout)  # Set the timeout in seconds
    try:
        result = function(*args, **kwargs)
    except TimeoutException:
        result = None
    finally:
        signal.alarm(0)  # Disable the alarm
    return result


def load_levels_from_file(filename):
    levels = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if not line.startswith("[") or not line.endswith("]"):
                print(f"{LINE_FORMAT_ERROR}: {line}")
                continue

            # Remove the outer brackets
            line = line[1:-1].strip()

            if not line:
                continue  # Skip empty lines

            dot_strings = line.split('), Dot')
            dots = []

            for dot_string in dot_strings:
                dot_string = dot_string.replace('Dot(', '').replace(')',
                                                                    '').strip()
                parts = dot_string.split(', ')

                if len(parts) == 4:
                    try:
                        x = int(parts[0].strip().lstrip(
                            '('))  # Strip any leading '('
                        y = int(parts[1].strip())
                        color = parts[2].strip("'")
                        connected = parts[3].strip() == 'True'
                        dots.append(Dot(x, y, color, connected))
                    except ValueError as e:
                        print(f"Error parsing line: {line}")
                        print(f"Details: {e}")
                        continue
            levels.append(dots)

    return levels


def print_results(algorithm, problems_not_passed_lst,
                  num_of_passed_problems, levels):
    print(f'{algorithm} passed {num_of_passed_problems}/{len(levels)}')
    if problems_not_passed_lst:
        print(f'problems not passed: {problems_not_passed_lst}')
    print('---------------------------------------------------')



def simulate_sat_solver(levels, grid_size):
    num_of_passed_problems = 0
    problems_not_passed_lst = []
    for level_num, level in enumerate(levels):
        colors, initial_board = convert_dots_to_sat_problem(level)
        sat_solver = FlowFreeSAT(grid_size, colors, initial_board)
        solution = sat_solver.solve(level)
        if solution == SAT_FAILED:
            problems_not_passed_lst.append(level_num)
            continue
        num_of_passed_problems += 1
    print_results("SAT", problems_not_passed_lst, num_of_passed_problems, levels)



def simulate_q_learning_solver(levels, grid_size):
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
                problems_not_passed_lst.append(level_num)

        print_results(algo, problems_not_passed_lst, problems_passed_counter)


def solve_search_problem(algo, problem_dots, grid_size):
    problem = FlowFreeProblem(grid_size, problem_dots)
    actions = run_with_timeout(3, run_search_algorithm, algo, problem)
    problem_state = problem.get_start_state()
    if actions is None:
        return problem_state
    for action in actions:
        problem_state = problem_state.do_move(action)
    return problem_state


def simulate_search_algorithm(levels, grid_size):
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
                problems_not_passed_lst.append(level_num)
        results[algo] = problems_passed_counter

        print_results(algo, problems_not_passed_lst,
                      problems_passed_counter, levels)

solvers = {"Search": simulate_search_algorithm,
           "SAT": simulate_sat_solver, "Q learning":
               simulate_q_learning_solver}


def simulate_all(grid_size, levels):
    for solver_type in solvers.keys():
            solvers.get(solver_type)(levels, grid_size)

def simulate_algorithms_for_grid_size(algorithm_type, grid_size,levels):
    if algorithm_type == "All":
        simulate_all(grid_size,levels)
    else:
        solvers.get(algorithm_type)(levels, grid_size)

if __name__ == "__main__":
    # for size in range(MIN_GRID_SIZE, MAX_GRID_SIZE):
    #     print("Simulating algorithms for grid size:", size)
    #     levels = load_levels_from_file(f'{PROBLEMS_DIR_NAME}/'
    #                                    f'{PROBLEM_FILE_PREFIX}-{size}.txt')
    #     algorithm_type = "Search"
    #     simulate_algorithms_for_grid_size(algorithm_type, size, levels)
    #     print()

    # for testing ##
    grid_size = 6
    levels = load_levels_from_file(f'{PROBLEMS_DIR_NAME}/'
                                    f'{PROBLEM_FILE_PREFIX}-{grid_size}.txt')
    for level in levels:
        problem = FlowFreeProblem(grid_size, level)
        display_initial_board(problem)



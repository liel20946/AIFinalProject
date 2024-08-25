from flow_game.flow_free_problem import FlowFreeProblem
from main import run_search_algorithm
from flow_game.dot import Dot
from main import convert_dots_to_sat_problem
from solvers.SAT import FlowFreeSAT
from main import choose_rl_agent
from main import display_initial_board

import signal

from solvers.flow_free_env import FlowFreeEnvironment




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
            line = line.strip()  # Remove leading/trailing whitespace
            if not line.startswith("[") or not line.endswith("]"):
                print(f"Unexpected line format: {line}")
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


def simulate_algorithms_for_grid_size(grid_size):
    # open the problems file
    levels = load_levels_from_file(f'problems/levels-{grid_size}.txt')
    # simulate_search_algorithm(levels, grid_size)
    # simulate_q_learning_solver(levels, grid_size)
    simulate_sat_solver(levels, grid_size)


def simulate_sat_solver(levels, grid_size):
    num_of_passed_problems = 0
    problems_not_passed_lst = []
    for level_num, level in enumerate(levels):
        colors, initial_board = convert_dots_to_sat_problem(level)
        sat_solver = FlowFreeSAT(grid_size, colors, initial_board)
        solution = sat_solver.solve(level)
        if solution == 'UNSAT':
            problems_not_passed_lst.append(level_num)
            continue
        num_of_passed_problems += 1

    print(f'SAT passed {num_of_passed_problems}/{len(levels)}')
    if problems_not_passed_lst:
        print(f'problems not passed: {problems_not_passed_lst}')
    print('---------------------------------------------------')


def simulate_q_learning_solver(levels, grid_size):
    q_algorithms = ["Q learning", "AQ learning"]
    results = {algo: 0 for algo in q_algorithms}
    for algo in q_algorithms:
        problems_not_passed_lst = []
        problems_passed_counter = 0
        for level_num, level in enumerate(levels):
            problem = FlowFreeProblem(grid_size, level)
            environment = FlowFreeEnvironment(problem)
            # Execute the solvers algorithm
            agent = choose_rl_agent(algo)
            # Train the agent
            agent.train(episodes=5000, environment=environment)
            # Solve a specific level
            initial_state = environment.reset()
            actions = agent.solve(initial_state, environment)
            problem_state = problem.get_start_state()
            for action in actions:
                problem_state = problem_state.do_move(action)
            if problem_state.is_goal_state():
                problems_passed_counter += 1
            else:
                problems_not_passed_lst.append(level_num)

        results[algo] = problems_passed_counter
        print(f'{algo} passed {problems_passed_counter}/{len(levels)}')
        if problems_not_passed_lst:
            print(f'problems not passed: {problems_not_passed_lst}')
        print('---------------------------------------------------')


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
        # print number of passed problems for each algorithm.
        # also print the problems that did not pass.
        print(f'{algo} passed {problems_passed_counter}/{len(levels)}')
        if problems_not_passed_lst:
            print(f'problems not passed: {problems_not_passed_lst}')
        print('---------------------------------------------------')


if __name__ == "__main__":
    for size in range(5, 6):
        print("Simulating algorithms for grid size:", size)
        simulate_algorithms_for_grid_size(size)
        print()

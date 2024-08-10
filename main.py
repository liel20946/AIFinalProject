import tkinter as tk
import time
from flow_game.flow_free_problem import FlowFreeProblem
from level_creator import get_level_dots
from solvers import solver
from solvers.q_learning_agent import QLearningAgent
from solvers.flow_free_env import FlowFreeEnvironment
from gui import FlowFreeGUI
import solvers.heuristics as heuristics
from solvers.approx_q_learning import ApproxQLearningAgent


def run_search_algorithm(search_algorithm_name, problem):
    if search_algorithm_name == "DFS":
        return solver.depth_first_search(problem)
    elif search_algorithm_name == "UCS":
        return solver.uniform_cost_search(problem)
    elif search_algorithm_name == "A*":
        return solver.a_star_search(problem, heuristics.combined_heuristic)
    elif search_algorithm_name == "BFS":
        return solver.breadth_first_search(problem)


def choose_rl_agent(agent_name):
    # TODO run a grid search on the parameters of the agents
    if agent_name == "Q learning":
        return QLearningAgent(0.7, 0.9, 0.75)
    elif agent_name == "AQ learning":
        return ApproxQLearningAgent()


def start_search(problem, algorithm_name):
    start_time = time.time()
    actions = run_search_algorithm(algorithm_name, problem)
    elapsed_time = time.time() - start_time
    return actions, elapsed_time


def execute_actions_with_delay(gui, curr_state, actions, index=0):
    if index < len(actions):
        action = actions[index]
        curr_state = curr_state.do_move(action)
        gui.update_board(curr_state.game_board)
        gui.root.after(500, lambda: execute_actions_with_delay(gui, curr_state,
                                                               actions,
                                                               index + 1))
    else:
        gui.display_win_message()  # Display "You Win" message when done


def solve_with_search():
    algorithm_name = "A*"
    dots_list, grid_size = get_level_dots(3, "easy")
    problem = FlowFreeProblem(grid_size, dots_list)
    display_initial_board(problem)

    # Execute the solvers algorithm
    # actions, elapsed_time = start_search(problem, algorithm_name)
    # display_gui(problem, algorithm_name, actions, elapsed_time)


def solve_with_rl():
    algorithm_name = "AQ learning"
    dots_list, grid_size = get_level_dots(2, "medium")
    problem = FlowFreeProblem(grid_size, dots_list)
    environment = FlowFreeEnvironment(problem)
    # Execute the solvers algorithm
    agent = choose_rl_agent(algorithm_name)
    # Train the agent
    agent.train(episodes=5000, environment=environment)
    # Solve a specific level
    initial_state = environment.reset()
    actions = agent.solve(initial_state, environment)

    display_gui(problem, algorithm_name, actions, 0)


def display_initial_board(problem):
    root = tk.Tk()
    board_size = problem.board.board_size
    gui = FlowFreeGUI(root, board_size, board_size)

    # Display the starting dots
    dots_list = problem.board.dots_list
    gui.display_starting_dots(dots_list)

    root.mainloop()


def display_gui(problem, algorithm_name, actions, elapsed_time):
    # Create Tkinter root and GUI only after the solvers algorithm is done
    root = tk.Tk()
    board_size = problem.board.board_size
    gui = FlowFreeGUI(root, board_size, board_size)

    # Set the solvers time, expanded nodes, and algorithm name in the GUI
    gui.set_search_time(elapsed_time)
    gui.set_expanded_nodes(problem.expanded)
    gui.set_algorithm_name(algorithm_name)

    if actions:
        # Display the initial state and start executing actions with a delay
        curr_state = problem.get_start_state()
        gui.update_board(curr_state.game_board)
        root.after(500, execute_actions_with_delay, gui, curr_state, actions)
    else:
        gui.display_lost_message()  # Display "You Lost" message if no actions

    root.mainloop()


def main():
    solve_with_search()
    # solve_with_rl()


if __name__ == "__main__":
    main()

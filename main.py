import tkinter as tk
import time
from flow_game.flow_free_problem import FlowFreeProblem
from level_creator import get_level_dots
from search import solver
from gui import FlowFreeGUI
import search.heuristics as heuristics


def run_search_algorithm(search_algorithm_name, problem):
    if search_algorithm_name == "DFS":
        return solver.depth_first_search(problem)
    elif search_algorithm_name == "UCS":
        return solver.uniform_cost_search(problem)
    elif search_algorithm_name == "A*":
        return solver.a_star_search(problem, heuristics.combined_heuristic)
    elif search_algorithm_name == "BFS":
        return solver.breadth_first_search(problem)


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
        gui.root.after(500, lambda: execute_actions_with_delay(gui, curr_state, actions, index + 1))
    else:
        gui.display_win_message()  # Display "You Win" message when done


def main():
    algorithm_name = "A*"
    dots_list, grid_size = get_level_dots(1, "medium")
    problem = FlowFreeProblem(grid_size, dots_list)

    # Execute the search algorithm
    actions, elapsed_time = start_search(problem, algorithm_name)

    # Create Tkinter root and GUI only after the search algorithm is done
    root = tk.Tk()
    board_size = problem.board.board_size
    gui = FlowFreeGUI(root, board_size, board_size)

    # Set the search time, expanded nodes, and algorithm name in the GUI
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


if __name__ == "__main__":
    main()
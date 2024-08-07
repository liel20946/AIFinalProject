import tkinter as tk
import time
from flow_free_problem import FlowFreeProblem
from level_creator import get_level_dots
import solver
from gui import FlowFreeGUI


def get_search_algorithm(search_algorithm_name):
    if search_algorithm_name == "DFS":
        return solver.depth_first_search
    elif search_algorithm_name == "UCS":
        return solver.uniform_cost_search
    elif search_algorithm_name == "A*":
        return solver.a_star_search
    elif search_algorithm_name == "BFS":
        return solver.breadth_first_search


def start_search(problem):
    start_time = time.time()
    search_algorithm = get_search_algorithm("DFS")
    actions = search_algorithm(problem)
    elapsed_time = time.time() - start_time
    return actions, elapsed_time


def execute_actions_with_delay(gui, curr_state, actions, index=0):
    if index < len(actions):
        action = actions[index]
        curr_state = curr_state.do_move(action)
        gui.update_board(curr_state.game_board)
        gui.increment_moves()  # Increment moves after the delay
        gui.root.after(500, lambda: execute_actions_with_delay(gui, curr_state, actions, index + 1))
    else:
        gui.display_win_message()  # Display "You Win" message when done


def main():
    dots_list = get_level_dots(5, "easy")
    problem = FlowFreeProblem(5, dots_list)

    # Execute the search algorithm
    actions, elapsed_time = start_search(problem)

    # Create Tkinter root and GUI only after the search algorithm is done
    root = tk.Tk()
    board_size = problem.board.board_size
    gui = FlowFreeGUI(root, board_size, board_size)

    # Set the search time in the GUI
    gui.set_search_time(elapsed_time)

    # Display the initial state and start executing actions with a delay
    curr_state = problem.get_start_state()
    gui.update_board(curr_state.game_board)
    root.after(500, execute_actions_with_delay, gui, curr_state, actions)
    root.mainloop()


if __name__ == "__main__":
    main()
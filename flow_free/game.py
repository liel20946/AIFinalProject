# main.py
import time
import tkinter as tk
from flow_free_problem import FlowFreeProblem
from dot import Dot
import solver
from gui import FlowFreeGUI


def start_search(problem, gui):
    curr_state = problem.get_start_state()
    gui.update_board(curr_state.game_board)
    gui.root.update()
    # Run DFS search with a delay for each action
    actions = solver.depth_first_search(problem)
    execute_actions_with_delay(gui, curr_state, actions)


def execute_actions_with_delay(gui, curr_state, actions, index=0):
    if index < len(actions):
        action = actions[index]
        curr_state = curr_state.do_move(action)
        gui.update_board(curr_state.game_board)
        gui.root.update()
        # Schedule the next action after 0.5 seconds
        gui.root.after(500, execute_actions_with_delay, gui, curr_state,
                       actions, index + 1)


def main():
    # Create the dots list with actual color names
    dots_list = [Dot(0, 0, 'red', False), Dot(4, 1, 'red', True),  # Red pair
                 Dot(3, 1, 'green', False), Dot(0, 2, 'green', True),
                 # Green pair
                 Dot(1, 2, 'blue', False), Dot(4, 2, 'blue', True),
                 # Blue pair
                 Dot(3, 3, 'yellow', False), Dot(0, 4, 'yellow', True),
                 # Yellow pair
                 Dot(1, 4, 'orange', False), Dot(4, 3, 'orange', True)
                 # Orange pair
                 ]
    problem = FlowFreeProblem(5, 5, dots_list)

    # Create Tkinter root and GUI
    root = tk.Tk()
    board_width = problem.board.board_w  # Get the width of the board
    board_height = problem.board.board_h  # Get the height of the board
    gui = FlowFreeGUI(root, board_width, board_height)

    # Display the initial state and start the search with a delay
    gui.update_board(problem.get_start_state().game_board)
    root.update()
    root.after(500, start_search, problem, gui)

    root.mainloop()


if __name__ == "__main__":
    main()

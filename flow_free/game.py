import tkinter as tk
from flow_free_problem import FlowFreeProblem
from dot import Dot
import solver
from gui import FlowFreeGUI


def start_search(problem, gui):
    curr_state = problem.get_start_state()
    gui.update_board(curr_state.game_board)
    actions = solver.depth_first_search(problem)
    execute_actions_with_delay(gui, curr_state, actions)


def execute_actions_with_delay(gui, curr_state, actions, index=0):
    if index < len(actions):
        action = actions[index]
        curr_state = curr_state.do_move(action)
        gui.update_board(curr_state.game_board)
        gui.root.after(500, lambda: execute_actions_with_delay(gui, curr_state, actions, index + 1))
        gui.increment_moves()  # Increment moves after the delay


def main():
    dots_list = [
        Dot(0, 0, 'red', False), Dot(4, 1, 'red', True),  # Red pair
        Dot(3, 1, 'green', False), Dot(0, 2, 'green', True),  # Green pair
        Dot(1, 2, 'blue', False), Dot(4, 2, 'blue', True),  # Blue pair
        Dot(3, 3, 'yellow', False), Dot(0, 4, 'yellow', True),  # Yellow pair
        Dot(1, 4, 'orange', False), Dot(4, 3, 'orange', True)  # Orange pair
    ]
    problem = FlowFreeProblem(5, 5, dots_list)

    root = tk.Tk()
    board_width = problem.board.board_w
    board_height = problem.board.board_h
    gui = FlowFreeGUI(root, board_width, board_height)

    gui.update_board(problem.get_start_state().game_board)
    root.after(500, start_search, problem, gui)
    root.mainloop()


if __name__ == "__main__":
    main()
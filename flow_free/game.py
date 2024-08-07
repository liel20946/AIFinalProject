import time

from flow_free_problem import FlowFreeProblem
from dot import Dot
import solver


def main():
    # create a simple flow free problem
    # create the dots list
    dots_list = [Dot(0, 0, 'R', False), Dot(4, 1, 'R', True),  # Red pair
                 Dot(3, 1, 'G', False), Dot(0, 2, 'G', True),
                 # Green pair
                 Dot(1, 2, 'B', False), Dot(4, 2, 'B', True),
                 # Blue pair
                 Dot(3, 3, 'Y', False), Dot(0, 4, 'Y', True),
                 # Yellow pair
                 Dot(1, 4, 'O', False), Dot(4, 3, 'O', True)
                 # Orange pair
                 ]
    # dots_list = [Dot(0, 0, 'R', False), Dot(4, 4, 'R', True)]  # Red pair]
    problem = FlowFreeProblem(5, 5, dots_list)
    curr_state = problem.get_start_state()

    # run dfs search
    actions = solver.depth_first_search(problem)

    for action in actions:
        curr_state = curr_state.do_move(action)
        print(curr_state)
        # delay 0.5 seconds
        time.sleep(0.5)

    print(curr_state)


if __name__ == "__main__":
     main()

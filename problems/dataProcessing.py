# from dataParser import parse_files
# from imageParser import parse_saved_files
# from util import normalize_array,denormalize_array
# import numpy as np
# from sklearn.model_selection import train_test_split
# import itertools
#
# def combine_data_files_and_images(max_board_size=25,file_list=[],img_list=[]):
#   problems1,solutions1 = parse_files(max_board_size=max_board_size,file_list=file_list)
#   problems2,solutions2 = parse_saved_files(max_board_size=max_board_size,file_list=img_list)
#   problems = problems1 + problems2
#   solutions = solutions1 + solutions2
#   return problems,solutions
#
# def generate_matrix_permutations(matrix,max_val):
#
#   def generate_symmetric_group_array(n):
#     return np.array([permutation for permutation in itertools.permutations([i for i in range(1,n+1)])])
#
#   def permute_matrix(matrix,permutation,n):
#     return np.array([permutation[i-1]*(matrix==i) for i in range(1,n+1)]).sum(axis=0)
#
#   matrices = []
#   sga = generate_symmetric_group_array(max_val)
#   for permutation in sga:
#     matrices.append(permute_matrix(matrix,permutation,max_val))
#   return matrices
#
# def generate_matrix_rotations(matrix):
#   rotations = []
#   for i in range(4):
#     rotations.append(np.rot90(matrix,i))
#     rotations.append(np.rot90(np.flip(matrix,i%2),i//2))
#   return rotations
#
# def process_data_for_training(max_board_size=15,file_list=[],with_permutations=False, with_rotations=False, test_size=0.05):
#     problems0,solutions0 = combine_data_files_and_images(max_board_size=max_board_size,file_list=file_list)
#     features=[]
#     labels=[]
#
#     max_val = np.max(problems0)  # note we are using 1-indexed colours here
#
#     if not with_permutations:
#       problems = problems0
#       solutions = solutions0
#     else:
#       problems = []
#       solutions = []
#       if with_rotations:
#         for problem in problems0:
#           for permutation in generate_matrix_permutations(problem,max_val):
#             for rotation in generate_matrix_rotations(permutation):
#               problems.append(rotation)
#         for solution in solutions0:
#           for permutation in generate_matrix_permutations(solution,max_val):
#             for rotation in generate_matrix_rotations(permutation):
#               solutions.append(rotation)
#       else:
#         for problem in problems0:
#           for permutation in generate_matrix_permutations(problem,max_val):
#             problems.append(permutation)
#         for solution in solutions0:
#           for permutation in generate_matrix_permutations(solution,max_val):
#             solutions.append(permutation)
#
#     features = np.array(problems).reshape(len(problems),max_board_size,max_board_size,1)
#     features = normalize_array(features,max_val)
#
#     labels = np.array(solutions).reshape(len(solutions),max_board_size*max_board_size,1)
#
#     del(problems)
#     del(solutions)
#
#     x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=test_size, random_state=42)
#     return x_train, x_test, y_train, y_test, max_val

class Dot:
    def __init__(self, x, y, color, is_goal):
        self.x = x
        self.y = y
        self.color = color
        self.is_goal = is_goal

    def __repr__(self):
        return f"Dot({self.x},{self.y},'{self.color}',{self.is_goal})"


def parse_board_configuration(board_config):
    size_part, prob_and_sol = board_config.split(':')
    start_positions, solution_path = prob_and_sol.split('=')
    size_x, size_y = map(int, size_part.split('x'))
    start_positions = list(map(int, start_positions.split(',')))
    solution_path = list(map(int, solution_path.split(',')))

    color_map = {
        0: 'red',
        1: 'blue',
        2: 'green',
        3: 'yellow',
        4: 'orange',
        5: 'purple',
        6: 'cyan',
        7: 'magenta',
        8: 'lime',
        9: 'pink',
        10: 'brown',
        11: 'gray',
        12: 'navy',
        13: 'teal',
        14: 'maroon',
        15: 'olive',
        16: 'coral',
        17: 'turquoise',
        18: 'violet',
        19: 'indigo'
    }

    dots = []
    color_last_position = {}

    for i in range(size_x):
        for j in range(size_y):
            value = start_positions[i * size_y + j]
            if value > 0:
                if value in color_last_position:
                    dots.append(Dot(i, j, color_map[value], True))
                else:
                    dots.append(Dot(i, j, color_map[value], False))
                color_last_position[value] = (i, j)

    return dots

def process_levels_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            dot_list = parse_board_configuration(line.strip())
            formatted_list = ', '.join(
                [f"Dot({dot.x}, {dot.y}, '{dot.color}', {dot.is_goal})" for dot in dot_list]
            )
            print(formatted_list)
            outfile.write(f"[{formatted_list}]\n")

if __name__ == "__main__":
    for i in range(5, 10):
        process_levels_file('image_paerser_output_{}.txt'.format(i),
                            'new_level_{}.txt'.format(i))


class Dot:
    def __init__(self, x, y, color, is_goal):
        self.x = x
        self.y = y
        self.color = color
        self.is_goal = is_goal


def parse_level(line):
    colors = ['red', 'green', 'blue', 'yellow', 'orange', 'pink', 'purple', 'cyan', 'magenta', 'black', 'white', 'gray', 'light blue', 'light green', 'light gray', 'dark blue', 'dark green', 'dark red', 'dark orange', 'gold', 'silver', 'brown', 'violet', 'indigo', 'sky blue', 'sea green', 'coral', 'turquoise', 'salmon', 'khaki', 'olive', 'teal', 'navy']

    parts = line.split('=')
    size_and_dots = parts[0]
    color_paths = parts[1].split('|')

    _, *dots = size_and_dots.split(';')

    dot_list = []
    for i in range(0, len(dots), 2):
        x1, y1 = map(int, dots[i].split(':'))
        x2, y2 = map(int, dots[i + 1].split(':'))
        color = colors[i]
        dot_list.append(Dot(x1 - 1, y1 - 1, color, False))  # Start dot
        dot_list.append(Dot(x2 - 1, y2 - 1, color, True))  # End dot

    return dot_list


def process_levels_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            dot_list = parse_level(line.strip())
            formatted_list = ', '.join(
                [f"Dot({dot.x}, {dot.y}, '{dot.color}', {dot.is_goal})" for dot in dot_list]
            )
            outfile.write(f"[{formatted_list}]\n")


if __name__ == "__main__":
    process_levels_file('data/image_parser_output.txt', 'levels.txt')

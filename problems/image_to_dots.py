import cv2
import random
import webcolors
from flow_game.dot import Dot


def closest_color(requested_color):
    """
    Find the closest color name to the requested color.
    :param requested_color: the color to find the closest color name to
    :return: the closest color name
    """
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def get_color_name(rgb_color):
    """
    Get the name of the color given its RGB values.
    :param rgb_color: the RGB values of the color
    :return: the name of the color
    """
    try:
        color_name = webcolors.rgb_to_name(rgb_color, spec='css3')
    except ValueError:
        color_name = closest_color(rgb_color)
    return color_name


def is_near_black(color, threshold=30):
    """
    Check if the color is near black.
    :param color: color to check
    :param threshold: threshold for near black
    :return: whether the color is near black
    """
    return all(c <= threshold for c in color)


def round_color(rgb_color, round_to=10):
    """
    Rounds the RGB values to the nearest multiple of `round_to`.
    :param rgb_color: rgb values to round
    :param round_to: multiple to round to
    :return: rounded rgb values
    """
    return tuple((round(channel / round_to) * round_to) for channel in rgb_color)


def convert_image_to_dots(image_path, grid_size):
    """
    Convert an image to a list of Dot objects.
    :param image_path: path to the image
    :param grid_size: size of the grid
    :return: list of Dot objects
    """
    # Load the image
    image = cv2.imread(image_path)
    # Convert the image to RGB (OpenCV loads images in BGR by default)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize a list to store Dot objects
    dots = []

    # Identify the grid cell size (assuming the image is perfectly aligned)
    height, width, _ = image.shape
    cell_width = width // grid_size
    cell_height = height // grid_size

    # Dictionary to store colors and their goal status
    color_to_dots = {}

    # Iterate over each cell in the grid
    for row in range(grid_size):
        for col in range(grid_size):
            # Calculate the center pixel of the cell
            center_x = col * cell_width + cell_width // 2
            center_y = row * cell_height + cell_height // 2

            # Get the color of the center pixel
            center_color = image[center_y, center_x]

            # Skip near-black colors
            if is_near_black(center_color):
                continue

            # Round the color to reduce sensitivity to small differences
            rounded_color = round_color(center_color)

            # Convert RGB to a web color name
            color_name = get_color_name(rounded_color)

            # Normalize color name to lowercase for consistent comparison
            color_name = color_name.lower()

            # Skip if color is black
            if color_name == 'black':
                continue

            # Create a Dot object for this cell
            dot = Dot(x=row, y=col, color=color_name, is_goal=False)
            dots.append(dot)
            if color_name in color_to_dots:
                color_to_dots[color_name].append(dot)
            else:
                color_to_dots[color_name] = [dot]

    # Randomly assign one of each color as the goal dot
    for color, dot_list in color_to_dots.items():
        goal_dot = random.choice(dot_list)
        goal_dot.is_goal = True

    return dots
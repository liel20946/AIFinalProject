class Dot:
    """
    A class to represent a dot in the game.
    """
    def __init__(self, x, y, color, is_goal):
        """
        Constructor for the Dot class.
        :param x: x coordinate of the dot
        :param y: y coordinate of the dot
        :param color: color of the dot
        :param is_goal: whether the dot is a goal dot
        """
        self.x = x
        self.y = y
        self.color = color
        self.is_goal = is_goal


    def get_x(self):
        """
        Getter for the x coordinate of the dot.
        :return: x coordinate of the dot
        """
        return self.x

    def get_y(self):
        """
        Getter for the y coordinate of the dot.
        :return: y coordinate of the dot
        """
        return self.y

    def get_color(self):
        """
        Getter for the color of the dot.
        :return: color of the dot
        """
        return self.color

    def get_is_goal(self):
        """
        Getter for whether the dot is a goal dot.
        :return: whether the dot is a goal dot
        """
        return self.is_goal

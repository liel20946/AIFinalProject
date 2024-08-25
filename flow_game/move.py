class Move:
    """
    Represents a move in the game. A move is a tuple of two points and a color.
    """
    def __init__(self, x, y, color):
        """
        Constructor for the Move class.
        :param x: x coordinate of the move
        :param y: y coordinate of the move
        :param color: color of the move
        """
        self.x = x
        self.y = y
        self.color = color

    def get_x(self):
        """
        Getter for the x coordinate of the move.
        :return: x coordinate of the move
        """
        return self.x

    def get_y(self):
        """
        Getter for the y coordinate of the move.
        :return: y coordinate of the move
        """
        return self.y

    def get_color(self):
        """
        Getter for the color of the move.
        :return: color of the move
        """
        return self.color

    def __eq__(self, other):
        """
        compares two moves
        :param other: the other move to compare to
        :return: whether the two moves are equal
        """
        return self.x == other.x and self.y == other.y and self.color == other.color

    def __hash__(self):
        """
        Hashes the move by its x, y and color.
        :return: hash of the move
        """
        return hash((self.x, self.y, self.color))

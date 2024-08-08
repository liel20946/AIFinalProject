class Move:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.color == other.color

    def __hash__(self):
        return hash((self.x, self.y, self.color))

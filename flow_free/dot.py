class Dot:
    def __init__(self, x, y, color, is_goal):
        self.x = x
        self.y = y
        self.color = color
        self.is_goal = is_goal


    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

    def get_is_goal(self):
        return self.is_goal

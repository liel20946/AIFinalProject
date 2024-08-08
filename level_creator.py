from flow_game.dot import Dot


def get_level_dots(set_number, difficulty):
    if difficulty == "easy":
        grid_size = 5
        if set_number == 1:
            return [
                Dot(0, 0, 'red', False), Dot(4, 1, 'red', True),
                Dot(3, 1, 'green', False), Dot(0, 2, 'green', True),
                Dot(1, 2, 'blue', False), Dot(4, 2, 'blue', True),
                Dot(3, 3, 'yellow', False), Dot(0, 4, 'yellow', True),
                Dot(1, 4, 'orange', False), Dot(4, 3, 'orange', True)
            ], grid_size
        elif set_number == 2:
            return [
                Dot(3, 1, 'red', False), Dot(0, 3, 'red', True),
                Dot(4, 2, 'green', False), Dot(3, 4, 'green', True),
                Dot(0, 0, 'blue', False), Dot(4, 1, 'blue', True),
                Dot(2, 2, 'yellow', False), Dot(1, 3, 'yellow', True),
                Dot(0, 4, 'orange', False), Dot(3, 2, 'orange', True)
            ], grid_size
        elif set_number == 3:
            return [
                Dot(0, 0, 'red', False), Dot(0, 3, 'red', True),
                Dot(2, 4, 'green', False), Dot(3, 2, 'green', True),
                Dot(4, 2, 'blue', False), Dot(4, 4, 'blue', True),
                Dot(4, 0, 'yellow', False), Dot(2, 3, 'yellow', True),
                Dot(0, 4, 'orange', False), Dot(3, 0, 'orange', True)
            ], grid_size

        elif set_number == -1:  # unsolvable
            return [
                Dot(0, 0, 'red', False), Dot(4, 1, 'red', True),
                Dot(3, 1, 'green', False), Dot(0, 2, 'green', True),
                Dot(0, 4, 'blue', False), Dot(4, 2, 'blue', True),
                Dot(3, 3, 'yellow', False), Dot(0, 4, 'yellow', True),
                Dot(1, 4, 'orange', False), Dot(4, 3, 'orange', True)
            ], grid_size

    elif difficulty == "medium":
        grid_size = 6
        if set_number == 1:
            return [
                Dot(4, 0, 'red', False), Dot(2, 2, 'red', True),
                Dot(3, 0, 'green', False), Dot(2, 5, 'green', True),
                Dot(3, 1, 'blue', False), Dot(1, 4, 'blue', True),
                Dot(2, 3, 'yellow', False), Dot(4, 4, 'yellow', True),
                Dot(2, 4, 'orange', False), Dot(5, 0, 'orange', True)
            ], grid_size
        elif set_number == 2:
            return [
                Dot(1, 0, 'red', False), Dot(5, 1, 'red', True),
                Dot(0, 2, 'green', False), Dot(0, 5, 'green', True),
                Dot(3, 4, 'blue', False), Dot(4, 5, 'blue', True),
                Dot(1, 2, 'yellow', False), Dot(3, 5, 'yellow', True),
                Dot(3, 1, 'orange', False), Dot(5, 2, 'orange', True),
                Dot(3, 2, 'light blue', False), Dot(5, 5, 'light blue', True),
                Dot(0, 0, 'pink', False), Dot(2, 4, 'pink', True),
            ], grid_size
        elif set_number == 3:
            return [
                Dot(0, 1, 'red', False), Dot(4, 1, 'red', True),
                Dot(5, 1, 'green', False), Dot(5, 5, 'green', True),
                Dot(0, 0, 'blue', False), Dot(5, 0, 'blue', True),
                Dot(1, 3, 'yellow', False), Dot(5, 4, 'yellow', True),
                Dot(1, 4, 'orange', False), Dot(4, 4, 'orange', True)
            ], grid_size

    elif difficulty == "hard":
        grid_size = 7
        if set_number == 1:
            return [
                Dot(2, 5, 'red', False), Dot(4, 2, 'red', True),
                Dot(0, 6, 'green', False), Dot(3, 0, 'green', True),
                Dot(1, 1, 'blue', False), Dot(3, 3, 'blue', True),
                Dot(2, 2, 'yellow', False), Dot(2, 6, 'yellow', True),
                Dot(2, 1, 'orange', False), Dot(1, 6, 'orange', True)
            ], grid_size
        elif set_number == 2:
            return [
                Dot(3, 1, 'red', False), Dot(2, 5, 'red', True),
                Dot(4, 1, 'green', False), Dot(3, 5, 'green', True),
                Dot(1, 1, 'blue', False), Dot(2, 6, 'blue', True),
                Dot(1, 0, 'yellow', False), Dot(5, 3, 'yellow', True),
                Dot(4, 3, 'orange', False), Dot(3, 5, 'orange', True),
                Dot(1, 0, 'purple', False), Dot(5, 3, 'purple', True),
                Dot(6, 0, 'light blue', False), Dot(6, 6, 'light blue', True),
            ], grid_size
        elif set_number == 3:
            return [
                Dot(0, 1, 'red', False), Dot(3, 3, 'red', True),
                Dot(0, 2, 'green', False), Dot(3, 0, 'green', True),
                Dot(3, 1, 'blue', False), Dot(5, 5, 'blue', True),
                Dot(1, 4, 'yellow', False), Dot(2, 1, 'yellow', True),
                Dot(1, 5, 'orange', False), Dot(4, 5, 'orange', True),
                Dot(0, 0, 'light blue', False), Dot(2, 0, 'light blue', True),
            ], grid_size



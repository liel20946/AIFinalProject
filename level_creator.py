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
                Dot(2, 4, 'red', False), Dot(4, 2, 'red', True),
                Dot(0, 5, 'green', False), Dot(3, 0, 'green', True),
                Dot(1, 1, 'blue', False), Dot(3, 3, 'blue', True),
                Dot(2, 2, 'yellow', False), Dot(2, 5, 'yellow', True),
                Dot(2, 1, 'orange', False), Dot(1, 5, 'orange', True)
            ], grid_size
        elif set_number == 2:
            return [
                Dot(3, 1, 'red', False), Dot(2, 4, 'red', True),
                Dot(4, 1, 'green', False), Dot(3, 4, 'green', True),
                Dot(1, 1, 'blue', False), Dot(2, 5, 'blue', True),
                Dot(1, 0, 'yellow', False), Dot(5, 3, 'yellow', True),
                Dot(4, 3, 'orange', False), Dot(3, 5, 'orange', True),
                Dot(2, 0, 'purple', False), Dot(5, 2, 'purple', True),
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

    elif difficulty == "very hard":
        grid_size = 8
        if set_number == 1:
            return [
                Dot(1, 1, 'red', False), Dot(3, 3, 'red', True),
                Dot(0, 7, 'green', False), Dot(2, 7, 'green', True),
                Dot(1, 7, 'blue', False), Dot(3, 5, 'blue', True),
                Dot(5, 1, 'yellow', False), Dot(6, 6, 'yellow', True),
                Dot(2, 5, 'orange', False), Dot(3, 1, 'orange', True),
                Dot(4, 3, 'pink', False), Dot(4, 5, 'pink', True),
                Dot(2, 1, 'light blue', False), Dot(3, 2, 'light blue', True),
            ], grid_size

    elif difficulty == "extreme":
        grid_size = 9
        if set_number == 1:
            return [
                Dot(1, 6, 'red', False), Dot(3, 6, 'red', True),
                Dot(2, 7, 'green', False), Dot(7, 7, 'green', True),
                Dot(3, 5, 'blue', False), Dot(5, 8, 'blue', True),
                Dot(3, 4, 'yellow', False), Dot(5, 7, 'yellow', True),
                Dot(1, 1, 'orange', False), Dot(6, 5, 'orange', True),
                Dot(1, 5, 'pink', False), Dot(7, 3, 'pink', True),
                Dot(0, 8, 'light blue', False), Dot(8, 0, 'light blue', True),
            ], grid_size
        elif set_number == 2:
            return [
                Dot(1, 3, 'red', False), Dot(3, 5, 'red', True),
                Dot(7, 0, 'green', False), Dot(8, 3, 'green', True),
                Dot(2, 6, 'blue', False), Dot(3, 3, 'blue', True),
                Dot(5, 3, 'yellow', False), Dot(5, 5, 'yellow', True),
                Dot(0, 7, 'orange', False), Dot(7, 7, 'orange', True),
                Dot(1, 4, 'pink', False), Dot(1, 6, 'pink', True),
                Dot(3, 6, 'light blue', False), Dot(7, 6, 'light blue', True),
                Dot(0, 8, 'cyan', False), Dot(8, 6, 'cyan', True),
                Dot(0, 6, 'brown', False), Dot(7, 5, 'brown', True),
                Dot(0, 1, 'purple', False), Dot(8, 5, 'purple', True),
            ], grid_size

        elif set_number == 3:
            return [
                Dot(4, 4, 'red', False), Dot(7, 4, 'red', True),
                Dot(1, 7, 'green', False), Dot(3, 1, 'green', True),
                Dot(5, 4, 'blue', False), Dot(6, 1, 'blue', True),
                Dot(4, 6, 'yellow', False), Dot(6, 6, 'yellow', True),
                Dot(2, 2, 'orange', False), Dot(4, 5, 'orange', True),
                Dot(3, 2, 'pink', False), Dot(3, 6, 'pink', True),
                Dot(4, 2, 'light blue', False), Dot(8, 0, 'light blue', True),
            ], grid_size

    elif difficulty == "12":
        grid_size = 12
        if set_number == 1:
            return [
                Dot(4, 5, 'red', False), Dot(9, 4, 'red', True),
                Dot(7, 9, 'green', False), Dot(4, 4, 'green', True),
                Dot(3, 3, 'blue', False), Dot(9, 12, 'blue', True),
                Dot(5, 11, 'yellow', False), Dot(11, 5, 'yellow', True),
                Dot(9, 10, 'orange', False), Dot(7, 7, 'orange', True),
                Dot(9, 3, 'purple', False), Dot(7, 1, 'purple', True),
                Dot(8, 1, 'cyan', False), Dot(11, 2, 'cyan', True),
                Dot(12, 5, 'pink', False), Dot(10, 12, 'pink', True),
                Dot(1, 12, 'brown', False), Dot(3, 12, 'brown', True)
            ], grid_size


    elif difficulty == "simple":
        if set_number == 2:
            grid_size = 4
            return [
                Dot(0, 0, 'red', False), Dot(3, 0, 'red', True),
                Dot(1, 1, 'green', False), Dot(3, 1, 'green', True)
            ], grid_size

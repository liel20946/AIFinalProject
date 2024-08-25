from flow_game.dot import Dot


def get_level_dots(grid_size, level):
    """
    Get the dots for the specified level and grid size.
    :param grid_size: size of the grid
    :param level: level number
    :return: list of dots for the specified level and grid size
    """
    if grid_size == 5:
        if level == 0:
            return [
                Dot(0, 0, 'red', False), Dot(0, 4, 'red', True),
                Dot(1, 0, 'blue', False), Dot(1, 4, 'blue', True),
                Dot(3, 1, 'green', False), Dot(3, 3, 'green', True),
            ]
        elif level == 1:
            return [
                Dot(0, 0, 'red', False), Dot(4, 1, 'red', True),
                Dot(3, 1, 'green', False), Dot(0, 2, 'green', True),
                Dot(1, 2, 'blue', False), Dot(4, 2, 'blue', True),
                Dot(3, 3, 'yellow', False), Dot(0, 4, 'yellow', True),
                Dot(1, 4, 'orange', False), Dot(4, 3, 'orange', True)
            ]
        elif level == 2:
            return [
                Dot(3, 1, 'red', False), Dot(0, 3, 'red', True),
                Dot(4, 2, 'green', False), Dot(3, 4, 'green', True),
                Dot(0, 0, 'blue', False), Dot(4, 1, 'blue', True),
                Dot(2, 2, 'yellow', False), Dot(1, 3, 'yellow', True),
                Dot(0, 4, 'orange', False), Dot(3, 2, 'orange', True)
            ]
        elif level == 3:
            return [
                Dot(0, 0, 'red', False), Dot(0, 3, 'red', True),
                Dot(2, 4, 'green', False), Dot(3, 2, 'green', True),
                Dot(4, 2, 'blue', False), Dot(4, 4, 'blue', True),
                Dot(4, 0, 'yellow', False), Dot(2, 3, 'yellow', True),
                Dot(0, 4, 'orange', False), Dot(3, 0, 'orange', True)
            ]
        elif level == 4:
            return [
                Dot(0, 0, 'blue', False), Dot(2, 2, 'green', False),
                Dot(3, 0, 'red', False), Dot(3, 1, 'green', True),
                Dot(3, 2, 'yellow', False), Dot(3, 4, 'blue', True),
                Dot(4, 0, 'yellow', True), Dot(4, 4, 'red', True)
            ]
        elif level == 5:
            return [
                Dot(1, 0, 'blue', False), Dot(1, 4, 'blue', True),
                Dot(0, 0, 'red', False), Dot(0, 4, 'red', True),
                Dot(3, 1, 'green', False), Dot(3, 3, 'green', True)
            ]

        elif level == 6:
            return [Dot(0, 0, 'purple', False), Dot(0, 2, 'green', False),
                    Dot(0, 4, 'yellow', False), Dot(1, 2, 'blue', False),
                    Dot(1, 4, 'orange', False), Dot(3, 1, 'green', True),
                    Dot(3, 3, 'yellow', True), Dot(4, 1, 'purple', True),
                    Dot(4, 2, 'blue', True), Dot(4, 3, 'orange', True)]
        elif level == -1:  # unsolvable
            return [
                Dot(0, 0, 'red', False), Dot(4, 1, 'red', True),
                Dot(3, 1, 'green', False), Dot(0, 2, 'green', True),
                Dot(0, 4, 'blue', False), Dot(4, 2, 'blue', True),
                Dot(3, 3, 'yellow', False), Dot(0, 4, 'yellow', True),
                Dot(1, 4, 'orange', False), Dot(4, 3, 'orange', True)
            ]

        elif level == -2:
            # just for testing
            return [Dot(0, 0, 'blue', False), Dot(2, 2, 'green', False),
                    Dot(3, 0, 'red', False), Dot(3, 1, 'green', True),
                    Dot(3, 2, 'yellow', False), Dot(3, 4, 'blue', True),
                    Dot(4, 0, 'yellow', True), Dot(4, 4, 'red', True)
                    ]


    elif grid_size == 6:
        if level == 1:
            return [
                Dot(4, 0, 'red', False), Dot(2, 2, 'red', True),
                Dot(3, 0, 'green', False), Dot(2, 5, 'green', True),
                Dot(3, 1, 'blue', False), Dot(1, 4, 'blue', True),
                Dot(2, 3, 'yellow', False), Dot(4, 4, 'yellow', True),
                Dot(2, 4, 'orange', False), Dot(5, 0, 'orange', True)
            ]
        elif level == 2:
            return [
                Dot(1, 0, 'red', False), Dot(5, 1, 'red', True),
                Dot(0, 2, 'green', False), Dot(0, 5, 'green', True),
                Dot(3, 4, 'blue', False), Dot(4, 5, 'blue', True),
                Dot(1, 2, 'yellow', False), Dot(3, 5, 'yellow', True),
                Dot(3, 1, 'orange', False), Dot(5, 2, 'orange', True),
                Dot(3, 2, 'light blue', False), Dot(5, 5, 'light blue', True),
                Dot(0, 0, 'pink', False), Dot(2, 4, 'pink', True),
            ]
        elif level == 3:
            return [
                Dot(0, 1, 'red', False), Dot(4, 1, 'red', True),
                Dot(5, 1, 'green', False), Dot(5, 5, 'green', True),
                Dot(0, 0, 'blue', False), Dot(5, 0, 'blue', True),
                Dot(1, 3, 'yellow', False), Dot(5, 4, 'yellow', True),
                Dot(1, 4, 'orange', False), Dot(4, 4, 'orange', True)
            ]
        elif level == 4:
            return [Dot(0, 1, 'purple', False), Dot(0, 2, 'blue', False),
                    Dot(0, 5, 'green', False), Dot(2, 2, 'orange', False),
                    Dot(2, 3, 'cyan', False), Dot(2, 5, 'green', True),
                    Dot(3, 3, 'yellow', False), Dot(3, 5, 'blue', True),
                    Dot(4, 1, 'cyan', True), Dot(4, 2, 'orange', True),
                    Dot(4, 4, 'yellow', True), Dot(4, 5, 'purple', True)]



    elif grid_size == 7:
        if level == 1:
            return [
                Dot(2, 4, 'red', False), Dot(4, 2, 'red', True),
                Dot(0, 5, 'green', False), Dot(3, 0, 'green', True),
                Dot(1, 1, 'blue', False), Dot(3, 3, 'blue', True),
                Dot(2, 2, 'yellow', False), Dot(2, 5, 'yellow', True),
                Dot(2, 1, 'orange', False), Dot(1, 5, 'orange', True)
            ]
        elif level == 2:
            return [
                Dot(3, 1, 'red', False), Dot(2, 4, 'red', True),
                Dot(4, 1, 'green', False), Dot(3, 4, 'green', True),
                Dot(1, 1, 'blue', False), Dot(2, 5, 'blue', True),
                Dot(1, 0, 'yellow', False), Dot(5, 3, 'yellow', True),
                Dot(4, 3, 'orange', False), Dot(3, 5, 'orange', True),
                Dot(2, 0, 'purple', False), Dot(5, 2, 'purple', True),
                Dot(6, 0, 'light blue', False), Dot(6, 6, 'light blue', True),
            ]
        elif level == 3:
            return [
                Dot(0, 1, 'red', False), Dot(3, 3, 'red', True),
                Dot(0, 2, 'green', False), Dot(3, 0, 'green', True),
                Dot(3, 1, 'blue', False), Dot(5, 5, 'blue', True),
                Dot(1, 4, 'yellow', False), Dot(2, 1, 'yellow', True),
                Dot(1, 5, 'orange', False), Dot(4, 5, 'orange', True),
                Dot(0, 0, 'light blue', False), Dot(2, 0, 'light blue', True),
            ]

    elif grid_size == 8:
        if level == 1:
            return [
                Dot(1, 1, 'red', False), Dot(3, 3, 'red', True),
                Dot(0, 7, 'green', False), Dot(2, 7, 'green', True),
                Dot(1, 7, 'blue', False), Dot(3, 5, 'blue', True),
                Dot(5, 1, 'yellow', False), Dot(6, 6, 'yellow', True),
                Dot(2, 5, 'orange', False), Dot(3, 1, 'orange', True),
                Dot(4, 3, 'pink', False), Dot(4, 5, 'pink', True),
                Dot(2, 1, 'light blue', False), Dot(3, 2, 'light blue', True),
            ]

    elif grid_size == 9:
        if level == 1:
            return [
                Dot(1, 6, 'red', False), Dot(3, 6, 'red', True),
                Dot(2, 7, 'green', False), Dot(7, 7, 'green', True),
                Dot(3, 5, 'blue', False), Dot(5, 8, 'blue', True),
                Dot(3, 4, 'yellow', False), Dot(5, 7, 'yellow', True),
                Dot(1, 1, 'orange', False), Dot(6, 5, 'orange', True),
                Dot(1, 5, 'pink', False), Dot(7, 3, 'pink', True),
                Dot(0, 8, 'light blue', False), Dot(8, 0, 'light blue', True),
            ]
        elif level == 2:
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
            ]

        elif level == 3:
            return [
                Dot(4, 4, 'red', False), Dot(7, 4, 'red', True),
                Dot(1, 7, 'green', False), Dot(3, 1, 'green', True),
                Dot(5, 4, 'blue', False), Dot(6, 1, 'blue', True),
                Dot(4, 6, 'yellow', False), Dot(6, 6, 'yellow', True),
                Dot(2, 2, 'orange', False), Dot(4, 5, 'orange', True),
                Dot(3, 2, 'pink', False), Dot(3, 6, 'pink', True),
                Dot(4, 2, 'light blue', False), Dot(8, 0, 'light blue', True),
            ]

    elif grid_size == 12:
        if level == 1:
            return [
                Dot(4, 2, 'red', False), Dot(2, 10, 'red', True),
                Dot(9, 6, 'blue', False), Dot(10, 10, 'blue', True),
                Dot(2, 9, 'light blue', False), Dot(4, 9, 'light blue', True),
                Dot(11, 3, 'yellow', False), Dot(2, 8, 'yellow', True),
                Dot(0, 8, 'orange', False), Dot(0, 11, 'orange', True),
                Dot(5, 6, 'purple', False), Dot(7, 2, 'purple', True),

                Dot(7, 1, 'white', False), Dot(9, 3, 'white', True),
                Dot(1, 1, 'pink', False), Dot(10, 9, 'pink', True),
                Dot(5, 2, 'brown', False), Dot(6, 5, 'brown', True),
                Dot(8, 8, 'grey', False), Dot(10, 8, 'grey', True),
                Dot(10, 0, 'green', False), Dot(11, 2, 'green', True),
                Dot(1, 5, 'dark green', False), Dot(2, 7, 'dark green', True),
                Dot(1, 6, 'light green', False), Dot(2, 3, 'light green',
                                                     True),

            ]

    elif grid_size == 14:
        if level == 1:
            return [
                Dot(5, 3, 'red', False), Dot(6, 7, 'red', True),
                Dot(8, 9, 'blue', False), Dot(11, 10, 'blue', True),
                Dot(6, 2, 'light blue', False), Dot(6, 4, 'light blue', True),
                Dot(1, 1, 'dark blue', False), Dot(1, 5, 'dark blue', True),
                Dot(2, 11, 'teal', False), Dot(5, 4, 'teal', True),
                Dot(8, 7, 'orange', False), Dot(10, 3, 'orange', True),
                Dot(4, 1, 'purple', False), Dot(12, 12, 'purple', True),
                Dot(7, 0, 'yellow', False), Dot(4, 10, 'yellow', True),
                Dot(8, 4, 'white', False), Dot(7, 11, 'white', True),
                Dot(10, 2, 'pink', False), Dot(11, 4, 'pink', True),
                Dot(13, 10, 'brown', False), Dot(10, 13, 'brown', True),
                Dot(13, 7, 'grey', False), Dot(9, 9, 'grey', True),
                Dot(3, 8, 'green', False), Dot(13, 9, 'green', True),
                Dot(9, 4, 'dark green', False), Dot(9, 7, 'dark green', True),
                Dot(5, 6, 'light green', False),
                Dot(7, 7, 'light green', True),
            ]

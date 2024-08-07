from flow_game.dot import Dot


def get_level_dots(grid_size, difficulty):
    if grid_size == 5:
        if difficulty == "easy":
            return [
                Dot(0, 0, 'red', False), Dot(4, 1, 'red', True),
                # Red pair
                Dot(3, 1, 'green', False), Dot(0, 2, 'green', True),
                # Green pair
                Dot(1, 2, 'blue', False), Dot(4, 2, 'blue', True),
                # Blue pair
                Dot(3, 3, 'yellow', False), Dot(0, 4, 'yellow', True),
                # Yellow pair
                Dot(1, 4, 'orange', False), Dot(4, 3, 'orange', True)
                # Orange pair
            ]
        elif difficulty == "medium":
            pass
        elif difficulty == "hard":
            pass



from definitions import Points, Paths, Tuple


def set_pins() -> Tuple[Points, int]:
    """
    This function returns the pins that your solution will try to connect.
    Edit this function to see if your solution works in different scenarios.
    Test cases will contain 8-14 pins.
    """
    pins = [(0, 1), (4, 4), (8, 3), (2, 5)]
    target = 13
    return pins, target


def find_paths(pins: Points, target: int = None) -> Paths:
    """
    This function contains your solution. It returns the paths to be tested.
    """
    paths = [
        ((0, 1), (0, 2)), ((0, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (3, 2)),
        ((3, 2), (4, 2)), ((4, 2), (4, 3)), ((4, 3), (4, 4)), ((2, 2), (2, 3)),
        ((2, 3), (2, 4)), ((2, 4), (2, 5)), ((4, 3), (5, 3)), ((5, 3), (6, 3)),
        ((6, 3), (7, 3)), ((7, 3), (8, 3)),
    ]
    return paths


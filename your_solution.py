from definitions import Points, Paths, Tuple


def find_paths(pins: Points, target: int = None) -> Tuple[Paths, int]:
    """
    This function contains your solution. It returns the paths to be tested.
    """
    # This is a hardcoded solution, make it smarter!
    paths = [
        ((0, 1), (0, 2)), ((0, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (3, 2)),
        ((3, 2), (4, 2)), ((4, 2), (4, 3)), ((4, 3), (4, 4)), ((2, 2), (2, 3)),
        ((2, 3), (2, 4)), ((2, 4), (2, 5)), ((4, 3), (5, 3)), ((5, 3), (6, 3)),
        ((6, 3), (7, 3)), ((7, 3), (8, 3)),
    ]
    flops = 1

    return paths, flops


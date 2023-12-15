from definitions import Points, Point, Paths, Tuple
from tqdm import tqdm
from random import randint, choice
from utils import flatten, manhattan_distance


def connect_two_points(point1: Point, point2: Point) -> Paths:
    (x1, y1), (x2, y2) = point1, point2
    # Horizontal (x) and and vertical (y) distance traveled
    diff_x, diff_y = x2 - x1, y2 - y1
    # Steps are all points covered by the path, so len(steps) = len(path) + 1
    steps = [(x1 + int(x * diff_x / abs(diff_x)), y1) for x in range(abs(diff_x) + 1)] if diff_x else []
    steps.extend([(x2, y1 + int(y * diff_y / abs(diff_y))) for y in range(abs(diff_y) + 1)] if diff_y else [])
    # zip all steps to create start and end points for paths
    paths = [s for s in zip(steps[:-1], steps[1:]) if s[0] != s[1]]
    return paths


def find_closest_points(points1, points2, rng=1):
    # Lists points by distance, randomly selects a point from the top `rng`
    p_comb = flatten([[(p1, p2) for p2 in points2 if p2 != p1] for p1 in points1])
    distances = {p: manhattan_distance(*p) for p in p_comb}
    dist_sorted_points = dict(sorted(distances.items(), key=lambda item: item[1]))
    random_closest = list(dist_sorted_points)[randint(0, rng)]
    return random_closest


def connect_pins(pins: Points, rng=0) -> Paths:
    # The goal is to build up a list of paths that connect all pins
    paths = []
    # Paths are started at pins...
    while any(pins):
        # ...and connected to any point in our paths.
        all_points = pins if not (any(paths)) else list(set(flatten(paths)))
        # The points we connect are the closest together
        points = find_closest_points(pins, all_points, rng=rng)[::choice([-1, 1])]
        # Our connection can be horizontal first or vertical first
        conns = connect_two_points(*points), connect_two_points(*points[::-1])
        # Find the connection that costs the least new paths
        paths.extend(min((set(conn) - set(paths) for conn in conns), key=len))
        # Update which points are not yet connected
        pins = [p for p in pins if p not in flatten(paths)]
    return paths


def run_search(pins, target=0, max_evals=100, rng=1):
    # Return the best solution that we've been able to find
    best_result = None
    for flops in tqdm(range(max_evals)):
        paths = connect_pins(pins, rng)
        if len(paths) <= target:
            best_result = paths
            break
        if best_result is None:
            best_result = paths
        elif len(paths) < len(best_result):
            best_result = paths
    return best_result, flops


def find_paths(pins: Points, target: int = None) -> Tuple[Paths, int]:
    """
    This function contains your solution. It returns the paths to be tested.
    """
    total_flops = 1
    for max_evals, rng in (
            (50, 0),
            (200, 1),
            (500, 2),
            (1000, 3),
            (10_000, 4),
            (100_000, 5),
            (1000_000, 6),
            (10_000_000, 7),
    ):
        paths, flops = run_search(pins, target, max_evals=max_evals, rng=rng)
        total_flops += flops
        if len(paths) <= target:
            break
    return paths, flops

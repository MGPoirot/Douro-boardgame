from definitions import Points, Paths, Tuple, Point
from typing import List
import numpy as np


def flatten(nested_list: List[List]) -> list:
    """
    Unnests a nested list.

    Parameters:
    - nested_list (List[List]): The nested list to be flattened.

    Returns:
    - list: Flattened list.

    Example:
    > flatten([[1], [2]])  # Returns [1, 2]
    """
    return [sub_list for sup_list in nested_list for sub_list in sup_list]


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
    pins, target = set_pins()
    pathfinder = PathFinder(pins, target)
    solution = pathfinder.solve(pins, target)
    return solution


class PathFinder:
    SIZE = 11
    BOARD = np.empty((SIZE, SIZE), dtype=tuple)

    # Fill the grid with coordinate tuples
    for i in range(SIZE):
        for j in range(SIZE):
            BOARD[i][j] = (i, j)

    def __init__(self, pins: Points, target: int = None):
        self.pins = pins
        self.target = target
        self.paths = []
        self.reduce_board()

    def reduce_board(self):
        """
        This function reduces the board to the smallest possible size.
        """
        self.board = self.BOARD[
            self.get_min_y(self.pins) : self.get_max_y(self.pins) + 1,
            self.get_min_x(self.pins) : self.get_max_x(self.pins) + 1,
        ]

    def inward_board(self):
        """
        This function reduces the board further by branching inwards.
        """
        for pin in self.pins:
            x, y = pin
            if x == self.get_min_x(self.pins) and x != 0:
                self.paths.append([(x, y), (x + 1, y)])
            if x == self.get_max_x(self.pins) and x != self.SIZE:
                self.paths.append([(x, y), (x - 1, y)])
            if y == self.get_min_y(self.pins) and y != 0:
                self.paths.append([(x, y), (x, y + 1)])
            if y == self.get_max_y(self.pins) and y != self.SIZE:
                self.paths.append([(x, y), (x, y - 1)])

    def find_paths(pins: Points, target: int = None) -> Paths:
        """
        This function contains your solution. It returns the paths to be tested.
        """

        def connect_two_points(point1: Point, point2: Point) -> Paths:
            (x1, y1), (x2, y2) = point1, point2
            diff_x, diff_y = x2 - x1, y2 - y1
            steps = (
                [
                    (x1 + int(x * diff_x / abs(diff_x)), y1)
                    for x in range(abs(diff_x) + 1)
                ]
                if diff_x
                else []
            )
            steps.extend(
                [
                    (x2, y1 + int(y * diff_y / abs(diff_y)))
                    for y in range(abs(diff_y) + 1)
                ]
                if diff_y
                else []
            )
            paths = [s for s in zip(steps[:-1], steps[1:]) if s[0] != s[1]]
            return paths

        paths = []
        for pin1, pin2 in zip(pins[1:], pins[:-1]):
            paths.extend(connect_two_points(point1=pin1, point2=pin2))
        return paths

    def solve(self, pins: Points, target: int = None) -> Paths:
        """
        Toplevel function that returns the solution.
        """
        solution = []
        return solution

    def set_probability(self, board: List[Points]) -> List[Points]:
        """
        This function sets the probability map for stochastic initiation.
        """

        return board

    def random_init(self, board: List[Points]) -> List[Points]:
        """
        This function randomly initiates the board.
        """

        return board

    @staticmethod
    def get_x(coords):
        try:
            coords[0][0][0]
            return [coord[0] for coord in flatten(coords)]
        except TypeError:
            return [coord[0] for coord in coords]

    @staticmethod
    def get_y(coords):
        try:
            coords[0][0][0]
            return [coord[1] for coord in flatten(coords)]
        except TypeError:
            return [coord[1] for coord in coords]

    def get_min_x(self, coords):
        return min(self.get_x(coords))

    def get_max_x(self, coords):
        return max(self.get_x(coords))

    def get_min_y(self, coords):
        return min(self.get_y(coords))

    def get_max_y(self, coords):
        return max(self.get_y(coords))

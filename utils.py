import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple, Dict
from definitions import Point, Points, Paths, colors, sorted_difficulties
from typing import Callable
from pathlib import Path
import matplotlib.cm as cm
import json
import argparse
import re


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


def sort_paths(paths: Paths) -> Paths:
    """
    Sorts points within paths to avoid duplicate paths like A -> B and B -> A.

    Parameters:
    - paths (Paths): List of paths, where each path is a tuple of two points (PathElement).

    Returns:
    - Paths: Sorted paths.

    Example:
    > sort_paths([((0, 1), (1, 0)), ((2, 3), (1, 2))])  # Returns [((0, 1), (1, 0)), ((1, 2), (2, 3))]
    """
    return [tuple(map(tuple, sorted(path, key=lambda x: (x[0], x[1])))) for path in paths]


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds"
    elif minutes > 0:
        return f"{int(minutes)} minutes, {seconds:.2f} seconds"
    else:
        return f"{seconds:.2f} seconds"


def rm_duplicate_pins(pins: Points) -> Points:
    """
  Removes duplicate pins from the list of pins.

  Parameters:
  - pins (Points): List of pins, where each pin is a point (Point).

  Returns:
  - Points: List of unique pins.

  Note:
  Prints a message if duplicates were found.

  Example:
  > rm_duplicate_pins([(0, 1), (2, 3), (0, 1)])  # Prints 'Pins contained 1 duplicate which was purged.'
  """
    n_non_unique = len(pins) - len(set(pins))
    if n_non_unique:
        was, s = ("was", "") if n_non_unique == 1 else ("were", "s")
        print(f'Pins contained {n_non_unique} duplicate{s} which {was} purged.')
    return list(set(pins))


def rm_duplicate_paths(paths: Paths) -> Paths:
    """
  Removes duplicate paths from the list of paths.

  Parameters:
  - paths (Paths): List of paths, where each path is a tuple of two points (PathElement).

  Returns:
  - Paths: List of unique paths.

  Note:
  Prints a message if duplicates were found.

  Example:
  > rm_duplicate_paths([((0, 1), (1, 0)), ((2, 3), (1, 2)), ((1, 0), (0, 1))])
  # Prints 'Paths contained 1 duplicate which was purged.' and returns [((0, 1), (1, 0)), ((1, 2), (2, 3))]
  """
    sorted_paths = sort_paths(paths)
    unique_paths = list(set(sorted_paths))
    n_non_unique = len(paths) - len(unique_paths)
    if n_non_unique:
        was, s = ("was", "") if n_non_unique == 1 else ("were", "s")
        print(f'Paths contained {n_non_unique} duplicate{s} which {was} purged.')
    return unique_paths


def manhattan_distance(point1: Point, point2: Point) -> int:
    """
  Computes Manhattan distance between two points.

  Parameters:
  - point1 (Point): First point (x, y).
  - point2 (Point): Second point (x, y).

  Returns:
  - int: Manhattan distance between the two points.

  Example:
  > manhattan_distance((0, 0), (1, 2))  # Returns 3
  """
    x1, y1 = point1
    x2, y2 = point2
    return int(abs(x2 - x1) + abs(y2 - y1))


def get_unique_filename(path: Path) -> Path:
    """
    Generate a unique filename by appending a number in parentheses.
    If the file exists, increment the number until a unique name is found.

    :param path: The original Path object.
    :return: A Path object with a unique filename.
    """
    if not path.exists():
        return path

    directory = path.parent
    name = path.stem
    extension = path.suffix

    counter = 2
    while True:
        new_name = f"{name} ({counter}){extension}"
        new_path = directory / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def scalar_to_color(scalar_list: list) -> list:
    """
    Converts scalars to colors for plotting purposes. (Not in use)

    Parameters:
    - scalar_list (list): List of scalar values.

    Returns:
    - list: List of colors corresponding to scalar values.

    Example:
    > scalar_to_color([0, 1, 2])  # Returns a list of colors mapped from the scalar values.
    """
    # Note: The function is not in use and may require modification based on specific use cases.
    # This example assumes matplotlib is available for color mapping.
    # The function may need further customization based on actual use.
    return cm.viridis([x / max(scalar_list) for x in scalar_list])


def validate_paths(paths: Paths, size=10) -> None:
    """
  Raises an error if the list of paths contains anything improperly formatted.

  Parameters:
  - paths (Paths): List of paths, where each path is a tuple of two points
    (PathElement).
  - size (int): Size of the board (number of tiles in each row/column).
    Default is 10.

  Raises:
  - TypeError: If paths is not of type list or if a path element is not a
    tuple.
  - ValueError: If a path element does not consist of a start and end point,
    if a point is not an x-y pair, if a value is not an integer, if a value is
    not an integer, if a value is less than 0 or greater than the specified
    size, or if a path element is not of length 1.

  Examples:
  > validate_paths([((0, 0), (0, 2))])  # Raises ValueError
  """
    if not isinstance(paths, list):
        raise TypeError(f'Paths should be of type list, but is of type {type(paths).__name__} {paths}.')
    for i, path in enumerate(paths):
        if not isinstance(path, tuple):
            raise TypeError(f'Path element {i} should be a tuple, but is a {type(path).__name__} {path}.')
        if not len(path) == 2:
            s = "" if len(path) == 1 else "s"
            raise ValueError(
                f'Path element {i} should consist of a start and end point. Instead it consists of {len(path)} point{s} {path}.')
        for point in path:
            if not isinstance(point, tuple):
                raise TypeError(
                    f'Path element {i} contained a point that was not a tuple, a {type(point).__name__} {path}.')
            if not len(point) == 2:
                s = "" if len(point) == 1 else "s"
                raise ValueError(
                    f'Path element {i} contained a point that was not an x-y pair, but {len(point)} value{s} instead {path}.')
            for value in point:
                if not isinstance(value, int) and not isinstance(value, float):
                    type_name = type(value).__name__
                    raise TypeError(
                        f'Path element {i} contained a value that was of type {type_name} and only ints and floats are accepted {path}.')
                if value % 1:
                    raise ValueError(f'Path element {i} contained a value that was not an integer {path}.')
                if value < 0:
                    raise ValueError(f'Path element {i} was not on the board ( < 0) {path}.')
                elif value > size:
                    raise ValueError(f'Path element {i} was not on the board ( > {size}) {path}.')
        path_length = manhattan_distance(*path)
        if path_length != 1:
            raise ValueError(f'Path element {i} should be of length 1, but is of length {path_length} ({path}).')





# TODO: give display_board info dict support
def display_board(
        paths: Paths = [],
        pins: Points = [],
        size=10,
        suptitle=None,
        path_colors=colors.path_blue,
        pin_colors=colors.pin_red,
        target: int = None,
        **kwargs,
) -> None:
    """
  Display a board with paths and pins.
  All parameters are optional.

  Parameters:
  - paths (Paths): List of paths, where each path is a list of points (PathElement).
  - pins (Points): List of pins, where each pin is a point (Point).
  - size (int): Size of the board (number of tiles in each row/column).
  - suptitle (str): Subtitle for the plot.
  - path_colors: Colors for paths, can be a string or a list of colors.
  - pin_colors: Colors for pins, can be a string or a list of colors.
  - target (int): Target number for successful connections.

  Returns:
  None
  """
    if 'paths' in kwargs:
        paths = kwargs['paths']
    if 'pins' in kwargs:
        pins = kwargs['pins']
    if 'kanten' in kwargs:
        target = kwargs['kanten']
    if 'size' in kwargs:
        size = kwargs['size']

    fig, ax = plt.subplots(figsize=(5, 4))
    # Drawing tiles
    be = 1  # Board edge width
    ax.add_patch(patches.Rectangle((-be / 2, -be / 2), size + be, size + be, fc=colors.tile_dark))
    for i in range(size):
        for j in range(size):
            rect = patches.Rectangle((i, j), 1, 1, lw=2, edgecolor=colors.tile_light, fc=colors.tile_dark)
            ax.add_patch(rect)

    # Drawing paths
    if any(paths):
        # Validate if the input data is correctly formatted
        validate_paths(paths, size=size)

        # Purge duplicate paths
        paths = rm_duplicate_paths(paths)

        # Convert single colors to list, or s
        if isinstance(path_colors, str):
            path_colors = [path_colors] * len(paths)
        elif not isinstance(path_colors[0], str):
            path_colors = scalar_to_color(path_colors)

        # Drawing paths
        for color, path in zip(path_colors, paths):
            (x1, y1), (x2, y2) = path
            if x1 == x2:  # Vertical path
                ax.plot([x1, x2], [min(y1, y2) + .15, max(y1, y2) - .15], c=color, lw=3)
            elif y1 == y2:  # Horizontal path
                ax.plot([min(x1, x2) + .15, max(x1, x2) - .15], [y1, y2], c=color, lw=3)
            else:
                print(f"Invalid path: {path}")

    # Drawing pin holes
    g = size + 1  # grid size
    ax.plot(flatten([range(g)] * g), flatten([[i] * g for i in range(g)]), '.k', ms=.5)

    # Drawing pins
    if any(pins):
        if isinstance(pin_colors, str):
            pin_colors = [pin_colors] * len(pins)
        elif not isinstance(pin_colors[0], str):
            pin_colors = scalar_to_color(pin_colors)

        pin_coords = np.array(pins).T
        ax.scatter(pin_coords[0], pin_coords[1], color=pin_colors, s=100, zorder=5)

    # Check if connections are successful
    msg = 'un'
    if any(paths) and any(pins):
        _, pin_clusters = get_clusters(paths, pins)
        n_clusters = len(set(pin_clusters.values()))
        if n_clusters == 1:
            msg = ''

    # Set x-axis labels as letters
    ax.set_xticks(np.arange(size) + .5)
    ax.set_xticklabels([chr(65 + i) for i in range(size)], fontsize=12)

    # Set y-axis labels as numerals
    ax.set_yticks(np.arange(size) + .5)
    ax.set_yticklabels(np.arange(1, size + 1), fontsize=12)

    # Turn off grids, set limits and make square
    ax.grid(False)
    ax.spines[:].set_visible(False)
    ax.set_aspect('equal')
    ax.set_xlim(-be / 2, size + be / 2)
    ax.set_ylim(-be / 2, size + be / 2)
    ax.tick_params(axis='both', which='both', length=0)

    # Set the figure title
    tgt = '' if target is None else f'/{target}'
    ttl = f'{msg}succesful with {len(paths)}{tgt} path elements'.capitalize()
    ttl = ttl if suptitle is None else f'{suptitle}\n{ttl}'
    ax.set_title(ttl)

    # Display image
    plt.show()


def unzip_name(name: str, **kwargs) -> dict:
    info = {k: v for k, v in [v.split('-') for v in name.split('_')]}
    fallbacks = {'name': 'unnamed',
                 'schwierigkeit': sorted_difficulties[0],
                 'size': 10,
                 'pins': 0,
                 'kanten': 0,
                 'version': 1,
                 }
    fallbacks.update(kwargs)

    for key, fallback in fallbacks.items():
        if key not in info:
            info[key] = fallback
        try:
            info[key] = int(info[key])
        except ValueError:
            pass
    if '-' in info.values() or '_' in info.values():
        raise ValueError(f'Illegal character ("_" or "-") in case properties:\n\t"{name}"')
    return info


def zip_name(info: dict) -> str:
    # Sanitize
    for k, v in info.items():
        if not isinstance(v, str) and not isinstance(v, int):
            del info[k]
    # Stringify
    return '_'.join((f'{k}-{str(v)}' for k, v in info.items()))





def score_solution(pins: Points, target: int, path_finder: Callable) -> Tuple[bool, int, Paths]:
    # Execute your solution
    paths = path_finder(pins, target)

    # Score the solution
    path_clusters, pin_clusters = get_clusters(paths, pins)

    # Check if all pins are in the same clusters
    is_success = len(set(pin_clusters.values())) == 1

    # Return if the solution was successful, and if so, how many paths were used.
    return is_success, len(paths), paths


def json_in(source: str):
    with open(source, 'r') as file:
        return json.load(file)


def json_out(obj: dict, target: str) -> None:
    with open(target, 'w') as file:
        json.dump(obj, file, indent=4, sort_keys=True)


def load_file(source: str):
    obj = json_in(source)
    if 'paths' in obj:
        obj['paths'] = [(tuple(i[0]), tuple(i[1])) for i in obj['paths']]
    if 'pins' in obj:
        obj['pins'] = [tuple(i) for i in obj['pins']]
    return obj


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the path finding solution.")
    parser.add_argument("filepath", nargs="?", default="None",
                        help="Module name where find_paths function is located. Default is 'your_solution'.")
    args = parser.parse_args()
    display_board(**load_file(args.filepath))

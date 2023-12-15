from typing import List, Tuple, Dict
from pathlib import Path
from typing import Callable
from timeit import default_timer
import json

# Object types
Point = Tuple[int, int]
Points = List[Point]
PathElement = Tuple[Point, Point]
Paths = List[PathElement]

sorted_difficulties = ['unbekannt', 'sehrleicht', 'leicht', 'mittel', 'schwer', 'sehrschwer', 'extremschwer']

project_root = Path.cwd()

solutions_root = project_root / 'solutions'

cases_dir = project_root / 'cases'
cases_dir.mkdir(exist_ok=True)



# Colors
class Colors:
    def __init__(self):
        self.path_blue = '#5f65ba'
        self.tile_dark = '#cd913b'
        self.tile_light = '#d7a053'
        self.pin_red = '#ca2801'

colors = Colors()





def get_clusters(paths: Paths, pins: Points = []) -> Tuple[Dict, Dict]:
    """
  Clusters pins and paths to common labels. For each, it returns a dictionary
  with points as keys and the cluster label as the value. Pins are optional.

  Parameters:
  - paths (Paths): List of paths, where each path is a tuple of points (PathElement).
  - pins (Points): List of pins, where each pin is a point (Point). Default is an empty list.

  Returns:
  A tuple containing two dictionaries:
  - path_clusters (Dict[Point, int]): A dictionary mapping points in paths to their cluster labels.
  - pin_clusters (Dict[Point, int]): A dictionary mapping pins to their cluster labels.

  Notes:
  This method is used to check success (all pins in the same cluster) but can
  also be used for visualization purposes.
  """
    # Validate input data
    if not isinstance(paths[0][0], tuple):
        raise ValueError(f'Invalid path data: {paths}, did you accidentally provide pin data inst')

    # Populate connections based on paths between pins
    point_owners = {}
    for i, points in enumerate(paths):
        for point in points:
            if point not in point_owners:
                point_owners[point] = [i]
            else:
                point_owners[point].append(i)

    label = 0
    path_clusters = {}
    while True:
        # Check if there are unvisited starting points
        starts = [path[0] for path in paths if path[0] not in path_clusters]
        if not any(starts):
            break
        # Perform a depth-first search (DFS) starting from the first pin
        to_visit = [starts[0]]
        while any(to_visit):
            point = to_visit.pop()
            path_clusters[point] = label
            for point_owner in point_owners[point]:
                for point in paths[point_owner]:
                    if point not in path_clusters:
                        to_visit.append(point)
        label += 1
    pin_clusters = {}
    for pin in pins:
        if pin not in path_clusters:
            pin_clusters[pin] = label
            label += 1
        else:
            pin_clusters[pin] = path_clusters[pin]
    return path_clusters, pin_clusters


class Cases(list):
    def __init__(self, n: int = None):
        for case_path in cases_dir.glob('*.json'):
            try:
                self.append(Case.from_json(case_path))
            except json.decoder.JSONDecodeError:
                raise ValueError(f'Invalid JSON in {case_path}')
            if n is not None and len(self) >= n:
                return


class Case:
    def __init__(self, file, pins=None, paths=None, **kwargs):
        self.file = file
        self.pins = pins if pins is not None else []
        self.paths = paths if paths is not None else []
        self.name = '_'.join((f'{k}-{str(v)}' for k, v in kwargs.items() if isinstance(v, str) or isinstance(v, int)))

        # Apply additional key-value pairs as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
            setattr(self, key, value)

    @classmethod
    def from_json(cls, case_path):
        """Load a Case object from a JSON file."""
        with open(case_path, 'r') as file:
            case = json.load(file)

        # Sanitize 'pins' and 'paths' if they exist
        if 'pins' in case:
            case['pins'] = [tuple(c) for c in case['pins']]
        if 'paths' in case:
            case['paths'] = [(tuple(p[0]), tuple(p[1])) for p in case['paths']]

        # Extract other attributes and pass them to the constructor
        return cls(case_path, **case)

    def solve(self, method: Callable) -> Tuple[bool, int, int, float]:
        start = default_timer()
        paths, flops = method(self.pins, self.kanten)
        stop = default_timer()

        d_time = stop - start

        # Score the solution
        path_clusters, pin_clusters = get_clusters(paths, self.pins)

        # Check if all pins are in the same clusters
        is_success = len(set(pin_clusters.values())) == 1

        if is_success:
            # Check existing score
            method_name = method.__module__
            solutions_file = solutions_root / method_name / self.file.name

            if solutions_file.is_file():
                is_better = len(paths) < len(Case(solutions_file).paths)
            else:
                is_better = True

            if is_better:
                # Save results
                solutions_file.parent.mkdir(exist_ok=True)
                data = self.__dict__.copy()
                data['file'] = str(solutions_file)
                data['paths'] = paths
                json_data = json.dumps(data, indent=4, sort_keys=True)
                with open(solutions_file, 'w') as file:
                    file.write(json_data)
        return is_success, len(paths), flops, d_time

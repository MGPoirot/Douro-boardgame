from definitions import Cases, solutions_root
from utils import format_time, get_unique_filename
import pandas as pd
import argparse
import importlib


def gen_result(solution_name: str) -> pd.DataFrame:
    solution_module = importlib.import_module(solution_name)
    target = solutions_root / solution_module.__name__ / 'test.csv'
    path_finder = getattr(solution_module, 'find_paths')

    # Define a data frame where we will store our results to
    case_attrs = ['name', 'schwierigkeit', 'size', 'kanten']
    score = pd.DataFrame(columns=case_attrs + ['pins', 'is_successful', 'paths_used', 'flops', 'time'])
    score.index.name = 'ID'

    for case in Cases():
        score.loc[case.id] = [getattr(case, c) for c in case_attrs] + [len(case.pins)] + list(case.solve(path_finder))
    score.to_csv(get_unique_filename(target))
    return score

solution_name='example_solution'
while True:
    gen_result(solution_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the path finding solution.")
    parser.add_argument("solution", nargs="?", default="your_solution",
                        help="Module name where find_paths function is located. Default is 'your_solution'.")
    args = parser.parse_args()
    score = gen_result(args.solution)

    # Display the score
    print('\n\n', score,
          f'\n\nTotal score:\n'
          f'- {int(score.is_successful.sum())}/{len(score)} successes\n'
          f'- {score.kanten.sum() - score.paths_used.sum()} paths\n'
          f'- {format_time(score.time.sum())} run time')




from utils import Points, score_solution, Tuple
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    # Define test data
    tests = {"schwierigkeit-leicht_pins-4_kanten-13": [(0, 1), (4, 4), (8, 3), (2, 5)], }

    # Sort difficulties in order
    difficulties = ['sehrleicht', 'leicht', 'mittel', 'schwer', 'sehrschwer', 'extremschwer']

    # Define a data frame where we will store our results to
    score = pd.DataFrame(
        columns=['schw_int', 'schwierigkeit', 'pins', 'kanten', 'is_successful', 'paths_used', 'score'])
    score.index.name = 'Test #'

    results = {}
    for i, (test_name, test_pins) in enumerate(tqdm(tests.items())):
        # Read the test description from the file name
        difficulty, pins, target = [k.split('-')[1] for k in test_name.split('_')][:3]

        # Make the pin reader return the test
        def set_pins() -> Tuple[Points, int]: return test_pins, target

        # Perform the test
        is_successful, paths_used, paths = score_solution()

        # Store the path found for later visualization
        results[test_name] = target, paths

        # Store test result in data frame
        score.loc[i] = [difficulties.index(difficulty), difficulty, pins, target, is_successful, paths_used,
                        int(target) - paths_used]

    # Sort the data frame by difficulty and drop the sorting column
    score = score.sort_values(by=['schw_int'], ascending=True)
    score = score.drop(columns=['schw_int'])

    # Display the score
    print('\n\n', score,
          f'\n\nTotal score: {score.is_successful.sum()}/{len(tests)} successes, with nett {score.score.sum()} paths.')

from utils import score_solution, set_pins, display_board

if __name__ == '__main__':
    # Calculate the score
    is_success, n_paths, paths = score_solution()

    # Print the score to the console
    if is_success:
        print(f'All pins were connected using {n_paths} path elements.\n')
    else:
        print('The paths did not connect all pins.\n')

    # Optional: visualize
    pins, target = set_pins()
    display_board(paths, pins, target=13)

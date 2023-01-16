import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='A small app to randomize a list of people.\n'
        + 'The people we choose from are in "./people.txt"'
    )
    parser.add_argument('exclude', type=str, nargs='*',
                        help='List of people to exclude')
    parser.add_argument('-f', '--fuzzyExclude', action='store_true',
                        help='Flag to use the exclude list as a fuzzy (not need to include whole name) or not')
    parser.add_argument('-o', '--order', type=str, nargs='+', default=[],
                        help='Allows you to specify a static list of people in the front, uses the fuzzy flag also')
    parser.add_argument('-t', '--testing', action='store_true',
                        help='Flag to write to a different file if testing new features')
    parser.add_argument('--file', type=str, default='',
                        help='Person file prefix, default blank')
    return parser.parse_args()

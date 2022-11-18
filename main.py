from random import random
from os import system as os_system, name as os_name
import argparse

def get_args () -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='A small app to randomize a list of people.\n'
        + 'The people we choose from are in "./people.txt"'
        )
    parser.add_argument('exclude', type=str, nargs='*', 
        help='List of people to exclude')
    args = parser.parse_args()
    return args

def get_file() -> list[str]:
    names = []
    with open('./.people.txt', 'r+') as file:
        data = file.read()
        names = data.split('\n')
    names = list(filter(lambda name: len(name) > 0, names))
    return names

def randomize (items: list[str]) -> list[str]:
    return list(sorted(items, key=lambda x: .5 - random()))

def clean (items: list[str], exclude: list[str]) -> list[str]:
    return [item for item in items if item not in exclude]

def main() -> None:
    os_system('cls' if os_name == 'nt' else 'clear')
    args = get_args()

    names = get_file()
    names = clean(names, args.exclude)
    names = randomize(names)

    print('\n'.join(names))

if __name__ == '__main__':
    main()
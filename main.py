from random import random
from os import system as os_system, name as os_name
import argparse
from datetime import datetime

def get_args () -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='A small app to randomize a list of people.\n'
        + 'The people we choose from are in "./people.txt"'
        )
    parser.add_argument('exclude', type=str, nargs='*', 
        help='List of people to exclude')
    parser.add_argument('-f', '--fuzzyExclude', action='store_true',
        help='Flag to use the exclude list as a fuzzy (not need to include whole name) or not')
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

def clean (names: list[str], exclude_list: list[str], fuzzy: bool) -> list[str]:
    if fuzzy:
        search_results = [*names]
        for exclude in exclude_list:
            matches = []
            for name in names:
                if exclude.lower() in name.lower():
                    matches.append(name)
            if len(matches) > 1:
                print(f'{exclude} had multiple matches: {", ".join(matches)}. No matches will be removed')
            elif len(matches) == 1:
                search_results = list(filter(lambda name: name not in matches, search_results))
        return search_results
    else:
        return [item for item in names if item not in exclude_list]

def transform_notes(notes: dict[str, list[str]]) -> str:
    data = ''
    for key, value in notes.items():
        data += f'## {key}\n'

        notes = list(filter(lambda note: note != '', value))
        if len(notes) == 0:
            notes = ['No notes or not present']
        data += ''.join(map(lambda note: f'- {note}\n', notes))
        data += '\n'
    
    return data

def take_notes(people: list[str]) -> None:
    data = {}

    for person in people:
        print(f'Notes for {person}:')
        data[person] = []
        while True:
            data[person].append(input('> '))

            if len(data[person]) >=2 and data[person][-2:] == ['', '']:
                break
    
    print()
    print(transform_notes(data))
    date = datetime.now()

    file_name = f'./notes/{date.date().isoformat()}.md'
    with open(file_name, 'w+') as file:
        file.write(transform_notes(data))
    
    print(f'wrote to file: "{file_name}"')

def main() -> None:
    os_system('cls' if os_name == 'nt' else 'clear')
    args = get_args()

    names = get_file()
    names = clean(names, args.exclude, args.fuzzyExclude)
    names = randomize(names)

    print(', '.join(map(lambda name: f'"{name}"', names)))
    print()

    take_notes(names)

if __name__ == '__main__':
    main()
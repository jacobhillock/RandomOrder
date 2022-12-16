from random import random
from os import system as os_system, name as os_name
from os.path import exists
import argparse
from datetime import datetime
from json import loads as loads_json
import re

def get_args () -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='A small app to randomize a list of people.\n'
        + 'The people we choose from are in "./people.txt"'
        )
    parser.add_argument('exclude', type=str, nargs='*', 
        help='List of people to exclude')
    parser.add_argument('-f', '--fuzzyExclude', action='store_true',
        help='Flag to use the exclude list as a fuzzy (not need to include whole name) or not')
    parser.add_argument('-t', '--testing', action='store_true',
        help='Flag to write to a different file if testing new features')
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

def add_list_header (line):
    list_regex = re.compile('^\s{2,}-')
    line += '\n'

    if (list_regex.findall(line)):
        return line
    return '- ' + line

def transform_notes(notes: dict[str, list[str]]) -> str:
    data = ''
    for key, value in notes.items():
        data += f'## {key}\n'

        notes = list(filter(lambda note: note != '', value))
        if len(notes) == 0:
            notes = ['No notes or not present']
        data += ''.join(map(add_list_header, notes))
        data += '\n'
    
    return data

def replace_key_tokens(notes: str) -> str:
    if not exists('./.tokens.json'):
        return notes
    tokens = {}
    with open('./.tokens.json', 'r') as file:
        tokens = loads_json(file.read())
        
    for key, value in tokens.items():
        # `?<=` means to capture after this group
        # `?=` means to capture after this group
        regex = re.compile(f'((?<=\s)({key})(?=\s))')
        notes = re.sub(regex, value, notes)

    return notes

def take_notes(people: list[str], testing: bool) -> None:
    data = {}

    for person in people:
        print(f'Notes for {person}:')
        data[person] = []
        while True:
            data[person].append(input('> '))

            if len(data[person]) >=2 and data[person][-2:] == ['', '']:
                break
    
    print()
    notes = transform_notes(data)
    notes = replace_key_tokens(notes)
    print(notes)
    date = datetime.now()

    file_name = f'./notes/{date.date().isoformat()}{"_t" if testing else ""}.md'
    with open(file_name, 'w+') as file:
        file.write(notes)
    
    print(f'wrote to file: "{file_name}"')

def main() -> None:
    args = get_args()
    os_system('cls' if os_name == 'nt' else 'clear')

    names = get_file()
    names = clean(names, args.exclude, args.fuzzyExclude)
    names = randomize(names)

    print(', '.join( names))
    print()

    take_notes(names, args.testing)

if __name__ == '__main__':
    main()
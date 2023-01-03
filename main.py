from random import random
from os import system as os_system, name as os_name
from os.path import exists
import argparse
from datetime import datetime
from json import loads as loads_json
import re


def get_args() -> argparse.Namespace:
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
    parser.add_argument('--file', type=str, default='',
                        help='Person file prefix, default blank')
    return parser.parse_args()


def get_file(prefix) -> list[str]:
    names = []
    with open(f'./{prefix}.people.txt', 'r+') as file:
        data = file.read()
        names = data.split('\n')
    names = list(filter(lambda name: len(name) > 0, names))
    return names


def randomize(items: list[str]) -> list[str]:
    return list(sorted(items, key=lambda x: .5 - random()))


def clean(names: list[str], exclude_list: list[str], fuzzy: bool) -> list[str]:
    if fuzzy:
        search_results = [*names]
        for exclude in exclude_list:
            matches = []
            for name in names:
                if exclude.lower() in name.lower():
                    matches.append(name)
            if len(matches) > 1:
                print(
                    f'{exclude} had multiple matches: {", ".join(matches)}. No matches will be removed')
            elif len(matches) == 1:
                search_results = list(
                    filter(lambda name: name not in matches, search_results))
        return search_results
    else:
        return [item for item in names if item not in exclude_list]


def add_list_header(line):
    list_regex = re.compile('^\s{2,}-')
    line += '\n'

    if (list_regex.findall(line)):
        return line
    return '- ' + line


def transform_notes(notes: dict[str, list[str]]) -> str:
    data = ''
    for key in sorted(notes.keys(), key=lambda k: k.split(' ')[-1]):
        value = notes[key]
        data += f'## {key}\n'

        notes_for_person = list(filter(lambda note: note != '', value))
        if len(notes_for_person) == 0:
            notes_for_person = ['No notes or not present']
        data += ''.join(map(add_list_header, notes_for_person))
        data += '\n'

    return data


def replace_key_tokens(notes: str, file_prefix: str) -> str:
    file_name = f'./{file_prefix}.tokens.json'

    if not exists(file_name):
        return notes
    tokens = {}
    with open(file_name, 'r') as file:
        tokens = loads_json(file.read())

    for key, value in tokens.items():
        # `?<=` means to capture after this group
        # `?=` means to capture after this group
        regex = re.compile(f'((?<=\W)({key})(?=\W))')
        notes = re.sub(regex, value, notes)

    return notes


def note_cmd_check(notes: list[str], cmd: list[str]):
    return len(notes) >= len(cmd) and notes[-1*len(cmd):] == cmd


def take_notes(people: list[str]) -> None:
    data = {}

    i = 0

    while i < len(people):
        # Prevent bound issues
        i = min(max(0, i), len(people) - 1)

        person = people[i]

        print(f'Notes for {person}:')
        for note in data.get(person, []):
            print(f'> {note}')
        while True:
            data[person] = data.get(person, list()) + [input('> ')]

            if note_cmd_check(data[person], ['', '']):
                i += 1
                break
            elif note_cmd_check(data[person], ['g', 'b']):
                data[person] = data[person][:-2]
                i -= 1
                break

    return data


def main() -> None:
    args = get_args()
    os_system('cls' if os_name == 'nt' else 'clear')

    names = get_file(args.file)
    names = clean(names, args.exclude, args.fuzzyExclude)
    names = randomize(names)

    print(', '.join(names), '\n')

    data_for_notes = take_notes(names)

    print()
    notes = transform_notes(data_for_notes)
    notes = replace_key_tokens(notes, args.file)

    print(notes)
    date = datetime.now()

    file_name = f'./notes/{date.date().isoformat()}' + \
        ("_t" if args.testing else "") + \
        (f'_{args.file}' if args.file != '' else "") + '.md'
    with open(file_name, 'w+') as file:
        file.write(notes)

    print(f'wrote to file: "{file_name}"')


if __name__ == '__main__':
    main()

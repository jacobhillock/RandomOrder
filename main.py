from random import random
from os import system as os_system, name as os_name

def get_file() -> list[str]:
    names = []
    with open('./.people.txt', 'r+') as file:
        data = file.read()
        names = data.split('\n')
    names = list(filter(lambda name: len(name) > 0, names))
    return names

def randomize (items: list[str]) -> list[str]:
    return list(sorted(items, key=lambda x: .5 - random()))


def main() -> None:
    os_system('cls' if os_name == 'nt' else 'clear')
    names = get_file()
    names = randomize(names)

    print('\n'.join(names))

if __name__ == '__main__':
    main()
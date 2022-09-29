import random
import os

def get_file() -> list[str]:
    names = []
    with open('./.people.txt', 'r+') as file:
        data = file.read()
        names = data.split('\n')
    return names

def main() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    names = get_file()
    while len(names) > 0:
        index = random.randint(0, len(names) - 1)
        print(names[index])
        del names[index]

if __name__ == '__main__':
    main()
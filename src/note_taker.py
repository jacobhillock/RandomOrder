from random import random
from src.args import get_args
from src.file_utils import FS
from src.logger import Logger
import re
from dataclasses import dataclass


@dataclass
class NotesConfig:
    file: str
    fuzzyExclude: bool
    exclude: list[str]
    front: list[str]
    log_level: str = 'WARN'
    empty_note: str = ''


class NoteTaker:
    def __init__(self, main_file: str, config: NotesConfig):
        self.config: NotesConfig = config
        self.main_file: str = main_file
        self.fs: FS = FS(main_file)
        self.log: Logger = Logger(
            main_file, self.fs.merge_file_paths('logs', 'log.txt'), config.log_level)
        self.notes: dict[str, list[str]] = {}
        self.__load_people()
        self.__load_tokens()

    def __load_people(self) -> None:
        self.log.INFO('Parsing people file')

        self.people_file = f'{self.config.file}.people.txt'
        self.log.INFO(f'{self.people_file=}')

        data: str = self.fs.get_file(self.people_file)
        names: list[str] = data.split('\n')
        names = list(filter(lambda name: len(name) > 0, names))
        self.log.INFO(f'from file_{names=}')

        fuzzy: bool = self.config.fuzzyExclude
        exclude_list: list[str] = self.config.exclude
        self.log.DEBUG(f'{fuzzy=} || {exclude_list=}')

        people: list[str] = []

        if fuzzy:
            search_results = [*names]
            for exclude in exclude_list:
                matches = []
                for name in names:
                    if exclude.lower() in name.lower():
                        matches.append(name)
                if len(matches) > 1:
                    self.log.WARN(
                        f'{exclude} had multiple matches: {", ".join(matches)}. No matches will be removed')
                elif len(matches) == 1:
                    search_results = list(
                        filter(lambda name: name not in matches, search_results))
            people = search_results
        else:
            people = [item for item in names if item not in exclude_list]
        self.log.INFO(f'{people=}')

        for person in people:
            self.notes[person] = list()

    def __load_tokens(self) -> None:
        self.token_file = f'{self.config.file}.tokens.json'
        self.log.INFO(f'{self.token_file=}')
        self.tokens = self.fs.get_json_file(self.token_file)
        self.log.INFO(f'{self.tokens=}')

    def __add_list_header(self, line: str) -> str:
        list_regex = re.compile('^\s{2,}-')
        line += '\n'

        if (list_regex.findall(line)):
            return line
        return '- ' + line

    def __get_front(self) -> list[str]:
        if len(self.config.front) == 0:
            return []

        names = list(self.notes.keys())
        front = []
        if self.config.fuzzyExclude:
            for fronts in self.config.front:
                matches = []
                for name in names:
                    if fronts.lower() in name.lower():
                        matches.append(name)
                if len(matches) > 1:
                    self.log.WARN(
                        f'{fronts} had multiple matches: {", ".join(matches)}. No matches will be removed')
                elif len(matches) == 1:
                    front.append(matches[0])
        else:
            front = [item for item in names if item in self.config.front]
        
        return front

    def randomize(self) -> list[str]:
        front = self.__get_front()

        print(f'{front=}')
        return front + list(sorted([person for person in self.notes.keys() if person not in front], key=lambda x: .5 - random()))

    def get_notes_for_person(self, name: str) -> list[str]:
        return self.notes.get(name, [])

    def set_notes_for_person(self, name: str, notes: list[str]) -> None:
        self.notes[name] = notes

    def add_note(self, name: str, note: str) -> None:
        if name not in self.notes.keys():
            self.log.WARN(f'{name=} not recognized from {self.notes.keys()}')
        self.notes[name] = [*self.notes.get(name, list()), note]

    def notes_as_md(self, sort_names: bool = False) -> str:
        markdown: str = ''
        people: list[str] = sorted(self.notes.keys(), key=lambda k: k.split(
            ' ')[-1]) if sort_names else list(self.notes.keys())

        for key in people:
            value = self.notes[key]
            markdown += f'## {key}\n'

            notes_for_person = list(filter(lambda note: note != '', value))
            if len(notes_for_person) == 0:
                notes_for_person = [self.config.empty_note]
            markdown += ''.join(map(self.__add_list_header, notes_for_person))
            markdown += '\n'

        for key in list(self.tokens.keys()):
            # `?<=` means to capture after this group
            # `?=` means to capture after this group
            regex = re.compile(f'((?<=\W)({key})(?=\W))')
            markdown = re.sub(regex, self.tokens[key], markdown)

        return markdown

    def __str__(self):
        return str(self.__dict__)

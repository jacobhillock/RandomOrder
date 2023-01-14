from os import name as os_name, makedirs as os_makedirs
from os.path import exists, dirname
from json import loads as loads_json


class FS:
    def __init__(self, relative_file: str):
        self.directory = relative_file.split(self.separator)[:-1]

    @property
    def separator(self) -> str:
        return '\\' if self.is_windows else '/'

    @property
    def is_windows(self) -> bool:
        return os_name == 'nt'

    def merge_file_paths(self, *file_paths: str) -> str:
        path = self.separator.join(file_paths)
        return path

    def get_file_path(self, file_name: str) -> str:
        return self.merge_file_paths(*self.directory, file_name)

    def get_file(self, file_name: str) -> str:
        file_path: str = self.get_file_path(file_name)

        if not self.exists(file_path=file_path):
            return ''

        file_data = ''
        with open(file_path, 'r') as file:
            file_data = file.read()
        return file_data

    def get_json_file(self, file_name: str) -> dict[str, str]:
        return loads_json(self.get_file(file_name))

    def write_file(self, file_name: str, contents: str, create_dir: bool = False) -> None:
        if create_dir:
            self.create_file(file_name, create_dir)
        file_path = self.get_file_path(file_name)
        with open(file_path, 'w+') as file:
            file.write(contents)

    def create_file(self, file_name: str, create_dir: bool = False) -> bool:
        file_path = self.get_file_path(file_name)
        dir_path = dirname(file_path)

        success = True

        if create_dir:
            os_makedirs(dir_path, exist_ok=True)

        # Create the file
        with open(file_path, 'a+') as file:
            pass

        return success

    def exists(self, file_name: str = '', file_path: str = '') -> bool:
        if file_path == '':
            file_path = self.get_file_path(file_name)

        return exists(file_path)

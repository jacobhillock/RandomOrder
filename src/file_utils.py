from os import name as os_name
from os.path import exists


class FS:
    def __init__(self, relative_file: str):
        self.directory = relative_file.split(FS.separator())[:-1]

    def separator() -> str:
        return '\\' if FS.is_windows else '/'

    @property
    def is_windows() -> bool:
        return os_name == 'nt'

    def get_file_path(self, file_name: str) -> str:
        return FS.separator().join(self.directory + [file_name])

    def get_file(self, file_name: str) -> str:
        file_path = self.get_file_path(file_name)

        if not self.exists(file_path=file_path):
            return ''

        file_data = ''
        with open(file_path, 'r') as file:
            file_data = file.read()
        return file_data

    def write_file(self, file_name: str, contents: str) -> None:
        file_path = self.get_file_path(file_name)
        with open(file_path, 'w+') as file:
            file.write(contents)

    def exists(self, file_name: str = '', file_path: str = '') -> bool:
        if file_path == '':
            file_path = self.get_file_path(file_name)

        return exists(file_path)

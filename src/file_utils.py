from os import name as os_name
from os.path import exists


class FS:
    def __init__(self, relative_file: str):
        self.separator = '\\' if FS.is_windows else '/'
        self.directory = relative_file.split(self.separator)[:-1]

    @property
    def is_windows() -> bool:
        return os_name == 'nt'

    def get_file_path(self, file_name: str) -> str:
        base_directory = self.separator.join(self.directory)
        file_path = f"{base_directory}{self.separator}{file_name}"
        return file_path

    def get_file(self, file_name: str) -> str:
        file_path = self.get_file_path(file_name)

        if not self.exists(file_path=file_path):
            return ''

        file_data = ''
        with open(file_path, 'r') as file:
            file_data = file.read()
        return file_data

    def exists(self, file_name: str = '', file_path: str = '') -> bool:
        if file_path == '':
            file_path = self.get_file_path(file_name)

        return exists(file_path)

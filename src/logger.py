from src.colors import colors
from src.file_utils import FS
import time
from typing import Optional

levels: dict[str, int] = {
    'DEBUG': 1,
    'INFO': 2,
    'WARN': 3,
    'ERROR': 4,
    'CRIT': 5
}


class Logger:
    def __init__(self, file_name: str, log_name: str, min_level: str = 'DEBUG'):
        self.file_name: str = file_name
        self.fs: FS = FS(self.file_name)
        self.log_name = log_name
        self.min_level: int = levels[min_level]
        self.do_print: bool = True
        self.fs.create_file(self.log_name, True)

    def toggle_print(self, print_value: Optional[bool] = None):
        if print_value == None:
            self.do_print = not self.do_print
        else:
            self.do_print = bool(print_value)

    def get_time(self, fmt: str = '%Y%m%dT%T') -> str:
        return time.strftime(fmt)

    def message_meta(self, severity: str) -> str:
        return f'[{self.get_time()}]{"_"*(5 - len(severity))}[{severity.upper()}]'

    def log(self, message: str, severity: str, color: str) -> None:
        if self.min_level > levels[severity]:
            return

        meta = self.message_meta(severity)
        if self.do_print:
            print(f'{color}{meta}{colors.reset} {message}')
        with open(self.fs.get_file_path(self.log_name), 'a+') as file:
            file.write(f'{meta} {message}\n')

    def INFO(self, message: str) -> None:
        self.log(message, 'INFO', f'{colors.fg.orange}')

    def DEBUG(self, message: str) -> None:
        self.log(message, 'DEBUG', f'{colors.fg.lightblue}')

    def WARN(self, message: str) -> None:
        self.log(message, 'WARN', f'{colors.fg.yellow}')

    def ERROR(self, message: str) -> None:
        self.log(message, 'ERROR', f'{colors.fg.lightred}')

    def CRIT(self, message: str) -> None:
        self.log(message, 'CRIT', f'{colors.fg.red}')

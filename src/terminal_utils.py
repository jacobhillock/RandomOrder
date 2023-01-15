from os import system as os_system
from src.file_utils import FS

def clear_screen():
    os_system('cls' if FS(__file__).is_windows else 'clear')

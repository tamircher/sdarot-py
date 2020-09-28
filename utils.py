import shutil
# import platform
from enum import Enum


def center(str):
    # if platform.system() == 'Windows':
    #     return str
    # else:
    terminal = shutil.get_terminal_size()
    return str.center(terminal.columns)


class ErrorCodes(Enum):
    UNKNOWN_ERROR = 1,
    HTTP_ERROR_301 = 2,
    NO_TOKEN = 3,
    NO_JSON = 4,
    SERVER_BUSY = 5

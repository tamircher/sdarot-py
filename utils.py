import shutil
import platform

def center(str):
    if platform.system() == 'Windows':
        return str
    else:
        terminal = shutil.get_terminal_size()
        return str.center(terminal.columns)

import shutil


def center(str):
    terminal = shutil.get_terminal_size()
    return str.center(terminal.columns)

# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          app.log.terminal.paths.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
from pathlib import PosixPath
# |--------------------------------------------------------------------------------------------------------------------|


class PathsLog(object):
    @staticmethod
    def show(path_: PosixPath) -> None:
        length_mode: int = 50
        path_: str = str(path_)
        if len(path_) < length_mode:
            path_ += " "*(length_mode - len(path_))
        elif len(path_) > length_mode:
            path_ = path_[0:47] + "..."
        
        print(f"read file: {Fore.CYAN}{path_}{Style.RESET_ALL}", end="")
    
    @staticmethod
    def close() -> None:
        print(f"{Fore.GREEN}{'[complete]'}{Style.RESET_ALL}")
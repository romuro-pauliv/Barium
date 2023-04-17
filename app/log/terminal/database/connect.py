# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               app.log.terminal.database.connect.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
# |--------------------------------------------------------------------------------------------------------------------|


class DBConnectLog(object):
    @staticmethod
    def show(uri: str) -> None:
        print(f"{Fore.MAGENTA}||| ")
        print(f"{Fore.MAGENTA}||| MONGODB CONNECT: {Fore.CYAN}{uri}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}||| {Style.RESET_ALL}")
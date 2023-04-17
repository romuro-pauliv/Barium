# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                              app.log.terminal.database.log.show.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
# |--------------------------------------------------------------------------------------------------------------------|


class LogDBLog(object):
    @staticmethod
    def show(chat_id: str, db: str, coll: str, log_key: str) -> None:
        method_: str = f"[{Fore.GREEN}POST{Style.RESET_ALL}]"
        db_terminal: str = f"[{Fore.GREEN}{db}{Style.RESET_ALL}]"
        coll_terminal: str = f"[{Fore.CYAN}{coll}{Style.RESET_ALL}]"
        log_key_terminal: str = f" -> '{log_key}'"
        print(f"{method_} {Fore.MAGENTA}||DB|| {Style.RESET_ALL}@{chat_id} {db_terminal}{coll_terminal}{log_key_terminal}")
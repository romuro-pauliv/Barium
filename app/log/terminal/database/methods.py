# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               app.log.terminal.database.methods.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
# |--------------------------------------------------------------------------------------------------------------------|


class MongoLog(object):
    @staticmethod
    def post(chat_id: str, db: str, coll: str, func: str) -> None:
        method_: str = f"[{Fore.LIGHTYELLOW_EX}PST{Style.RESET_ALL}]"
        db_info: str = f"|{Fore.MAGENTA} DB {Style.RESET_ALL}|"
        chat_id_terminal: str = f"{Fore.LIGHTCYAN_EX}@{chat_id}{Style.RESET_ALL}"
        func_terminal: str = f"-> {Fore.GREEN}{func}{Style.RESET_ALL}"
        
        db_terminal: str = f"[{Fore.GREEN}{db}{Style.RESET_ALL}]"
        coll_terminal: str = f"[{Fore.CYAN}{coll}{Style.RESET_ALL}]"
        
        print(f"{method_} {chat_id_terminal} {db_info} {db_terminal}{coll_terminal} {func_terminal}")
    
    @staticmethod
    def get(chat_id: str, db: str, coll: str, func: str) -> None:
        method_: str = f"[{Fore.LIGHTGREEN_EX}GET{Style.RESET_ALL}]"
        db_info: str = f"|{Fore.MAGENTA} DB {Style.RESET_ALL}|"
        chat_id_terminal: str = f"{Fore.LIGHTCYAN_EX}@{chat_id}{Style.RESET_ALL}"
        func_terminal: str = f"<- {Fore.GREEN}{func}{Style.RESET_ALL}"
        
        db_terminal: str = f"[{Fore.GREEN}{db}{Style.RESET_ALL}]"
        coll_terminal: str = f"[{Fore.CYAN}{coll}{Style.RESET_ALL}]"
        
        print(f"{method_} {chat_id_terminal} {db_info} {db_terminal}{coll_terminal} {func_terminal}")
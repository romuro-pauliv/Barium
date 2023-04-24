# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 app.log.cache.internal.sessions.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
from typing import Any
import sys
# |--------------------------------------------------------------------------------------------------------------------|


class InternalSession(object):
    @staticmethod
    def post(chat_id: str, var: Any) -> None:
        cache_info: str = f"| {Fore.YELLOW}[SESSION]{Style.RESET_ALL}"
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL}"
        input_terminal: str = f"[{Fore.LIGHTYELLOW_EX}PST{Style.RESET_ALL}]"    
        bytes_terminal: str = f"SIZE: [{Fore.YELLOW}{str(sys.getsizeof(var))}B{Style.RESET_ALL}]"
        
        print(f"{input_terminal} {chat_id_terminal} {cache_info} {bytes_terminal}")
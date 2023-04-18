# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                           app.log.cache.internal.cache_variable.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
from typing import Any
import sys
# |--------------------------------------------------------------------------------------------------------------------|


class InternalCacheLog(object):
    @staticmethod
    def post(chat_id: str, instance: str, var: Any) -> None:
        cache_info: str = f"| {Fore.BLUE}VAR-CACHE{Style.RESET_ALL}"
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL}"
        input_terminal: str = f"[{Fore.LIGHTYELLOW_EX}PST{Style.RESET_ALL}]"
        instance_terminal: str = f"| {instance} |"    
        bytes_terminal: str = f"SIZE: [{Fore.YELLOW}{str(sys.getsizeof(var))}B{Style.RESET_ALL}]"

        print(f"{input_terminal} {chat_id_terminal} {cache_info} {instance_terminal} {bytes_terminal}")
    
    @staticmethod
    def get(chat_id: str, instance: str, var: Any) -> None:
        cache_info: str = f"| {Fore.BLUE}VAR-CACHE{Style.RESET_ALL}"
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL}"
        input_terminal: str = f"[{Fore.LIGHTGREEN_EX}GET{Style.RESET_ALL}]"
        instance_terminal: str = f"| {instance} |"    
        bytes_terminal: str = f"SIZE: [{Fore.YELLOW}{str(sys.getsizeof(var))}B{Style.RESET_ALL}]"

        print(f"{input_terminal} {chat_id_terminal} {cache_info} {instance_terminal} {bytes_terminal}")
    
    @staticmethod
    def delete(chat_id: str, instance: str, var: Any) -> None:
        cache_info: str = f"| {Fore.BLUE}VAR-CACHE{Style.RESET_ALL}"
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL}"
        input_terminal: str = f"[{Fore.LIGHTRED_EX}DEL{Style.RESET_ALL}]"
        instance_terminal: str = f"| {instance} |"    
        bytes_terminal: str = f"SIZE: [{Fore.YELLOW}{str(sys.getsizeof(var))}B{Style.RESET_ALL}]"

        print(f"{input_terminal} {chat_id_terminal} {cache_info} {instance_terminal} {bytes_terminal}")
        
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                            app.log.terminal.cache.redis.methods.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
# |--------------------------------------------------------------------------------------------------------------------|


class RedisCacheLog(object):
    @staticmethod
    def post(chat_id: str, instance: str) -> None:
        cache_info: str = f"| {Fore.MAGENTA}REDIS{Style.RESET_ALL}"
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL}"
        input_terminal: str = f"[{Fore.LIGHTYELLOW_EX}PST{Style.RESET_ALL}]"
        instace_terminal: str = f" >>> {instance}"
        
        print(f"{input_terminal} {chat_id_terminal} {cache_info} {instace_terminal}")
    
    @staticmethod
    def get(chat_id: str, instance: str) -> None:
        cache_info: str = f"| {Fore.MAGENTA}REDIS{Style.RESET_ALL}"
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL}"
        input_terminal: str = f"[{Fore.LIGHTGREEN_EX}GET{Style.RESET_ALL}]"
        instace_terminal: str = f" >>> {instance}"
        
        print(f"{input_terminal} {chat_id_terminal} {cache_info} {instace_terminal}")
    
    @staticmethod
    def delete(chat_id: str, instance: str) -> None:
        cache_info: str = f"| {Fore.MAGENTA}REDIS{Style.RESET_ALL}"
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL}"
        input_terminal: str = f"[{Fore.LIGHTRED_EX}DEL{Style.RESET_ALL}]"
        instace_terminal: str = f" >>> {instance}"
        
        print(f"{input_terminal} {chat_id_terminal} {cache_info} {instace_terminal}")
    
    
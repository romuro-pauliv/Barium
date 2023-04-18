# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                             app.log.terminal.redis.login_cached.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
# |--------------------------------------------------------------------------------------------------------------------|

class LoginCachedLog(object):
    @staticmethod
    def read(database: str) -> None:
        length_mode: int = 20
        if len(database) < length_mode:
            database += " "*(length_mode - len(database))
        elif len(database) > length_mode:
            database = database[0:17] + "..."
        
        print(f"read: {Fore.YELLOW}{database}{Style.RESET_ALL} || ", end="")

    @staticmethod
    def false() -> None:
        print(f"{Fore.RED}{'FALSE'}{Style.RESET_ALL}")
    
    @staticmethod
    def active() -> None:
        print(f"{Fore.GREEN}{'ACTIVE'}{Style.RESET_ALL}")
    
    @staticmethod
    def add_in_cache(chat_id: str) -> None:
        length_mode: int = 20
        if len(chat_id) < length_mode:
            chat_id += " "*(length_mode - len(chat_id))
        elif len(chat_id) > length_mode:
            chat_id = chat_id[0:17] + "..."

        print(f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL} >>> {Fore.CYAN}REDIS{Style.RESET_ALL} CACHE")
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                            app.log.terminal.redis.redis_connect.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
# |--------------------------------------------------------------------------------------------------------------------|


class RedisConnectLog(object):
    @staticmethod
    def show(host: str, port: str, db: int) -> None:
        print(f"{Fore.CYAN}REDIS{Style.RESET_ALL}: {host}:{Fore.CYAN}{port}{Fore.YELLOW} DB({db}){Style.RESET_ALL}")
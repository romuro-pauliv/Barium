# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       app.utils.process_monitor.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Any

from colorama import Fore, Style
import datetime
import time

from resources.data import LOG_REPORT
# |--------------------------------------------------------------------------------------------------------------------|


class ProcessMonitor:
    def __init__(self) -> None:
        self.text_data: dict[str, Any] = LOG_REPORT['process_monitor']
        self.init_start_time: float = 0
        self.init_finish_time: float = 0
        
    def init_process_start(self) -> None:
        """
        Starts the initialization process and prints the corresponding message.
        """
        text_data: str = self.text_data['init']
        prefix: str = f"{Fore.GREEN}[*]{Style.RESET_ALL}"
        text: str = f"{text_data[0]}{Fore.CYAN}{text_data[1]}{Style.RESET_ALL}{text_data[2]}"
        print(prefix, text, end="")
        self.init_start_time: float = time.time()
    
    def init_process_finish(self) -> None:
        """
        Finishes the initialization process and prints the elapsed time in milliseconds.
        """
        print(round((time.time() - self.init_start_time)*1000, 2), "ms")
    
    def clock_process_start(self) -> None:
        """
        Starts the clock process.
        """
        self.clock_start_time: float = time.time()
    
    def clock_process_finish(self, username: str, telegram_update: bool = False) -> None:
        """
        Finishes the clock process and prints the elapsed time in milliseconds along with relevant information.
        
        Args:
            username (str): The username associated with the clock process.
            telegram_update (bool): Indicates if it's a Telegram update.
        """
        text_data: str = self.text_data["clock"]
        prefix: str = f"{Fore.MAGENTA}[-]{Style.RESET_ALL}"
        date: str = str(datetime.datetime.now())
        
        if telegram_update:
            text: str = f"- {Fore.MAGENTA}{'telegram_update'}{Style.RESET_ALL}"
        else:
            text: str = f"- {text_data[0]}{Fore.MAGENTA}{username}{Style.RESET_ALL}"
        
        clock_text: str = str(round((time.time() - self.clock_start_time)*1000, 2))
        
        print(prefix, date, text, clock_text, "ms")
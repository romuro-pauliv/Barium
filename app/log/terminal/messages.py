# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       app.log.terminal.messages.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
import unicodedata
import datetime
# |--------------------------------------------------------------------------------------------------------------------|


class MessagesLog(object):
    @staticmethod
    def received_message(chat_id: str, msg: str) -> None:
        msg_length: int = 30
        indicator_terminal: str = f"[{Fore.LIGHTBLUE_EX}<<<{Style.RESET_ALL}] "
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL} | "
        datetime_terminal: str = f"{datetime.datetime.utcnow()} | "
        
        if not isinstance(msg, str):
            msg: str = "BIN MODE"
        
        if len(msg) < msg_length:
            msg += " "*(msg_length - len(msg))
        elif len(msg) > msg_length:
            msg = msg[0:27] + "..."
        
        msg = msg.replace("\n", " ")
        
        new_text: str = ""
        for char in msg:
            if char == " " or unicodedata.category(char)[0] != "S":
                new_text += char
        
        msg: str = new_text
        
        msg_terminal: str = f"| {Fore.LIGHTBLUE_EX}{msg}{Style.RESET_ALL} |"
        
        print(f"{indicator_terminal}{chat_id_terminal}{datetime_terminal}{msg_terminal}")
    
    @staticmethod
    def send_message(chat_id: str, msg: str) -> None:
        msg_length: int = 30
        indicator_terminal: str = f"[{Fore.GREEN}>>>{Style.RESET_ALL}] "
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL} | "
        datetime_terminal: str = f"{datetime.datetime.utcnow()} | "
        
        if not isinstance(msg, str):
            msg: str = "BIN MODE"
        
        msg: str = msg.replace("\n", " ")
        
        new_text: str = ""
        for char in msg:
            if char == " " or unicodedata.category(char)[0] != "S":
                new_text += char
        
        msg: str = new_text
        
        if len(msg) < msg_length:
            msg += " "*(msg_length - len(msg))
        elif len(msg) > msg_length:
            msg = msg[0:27] + "..."
        
        msg_terminal: str = f"| {Fore.GREEN}{msg}{Style.RESET_ALL} |"
        
        print(f"{indicator_terminal}{chat_id_terminal}{datetime_terminal}{msg_terminal}")
    
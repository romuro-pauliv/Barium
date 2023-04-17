from colorama import Fore, Style
import datetime

chat_id: str = "1231231231"


class MessagesLog(object):
    @staticmethod
    def received_message(chat_id: str, msg: str) -> None:
        msg_length: int = 30
        indicator_terminal: str = f"[{Fore.LIGHTBLUE_EX}<<<{Style.RESET_ALL}] "
        chat_id_terminal: str = f"{Fore.MAGENTA}@{chat_id}{Style.RESET_ALL} | "
        datetime_terminal: str = f"{datetime.datetime.utcnow()} | "
        
        if len(msg) < msg_length:
            msg += " "*(msg_length - len(msg))
        elif len(msg) > msg_length:
            msg = msg[0:27] + "..."
        
        msg_terminal: str = f"| {Fore.LIGHTBLUE_EX}{msg}{Style.RESET_ALL} |"
        
        print(f"{indicator_terminal}{chat_id_terminal}{datetime_terminal}{msg_terminal}")

        
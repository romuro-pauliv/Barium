# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               app.models.models.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramMessages, Tools
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list
# |--------------------------------------------------------------------------------------------------------------------|


class TextValidation(object):
    def __init__(self) -> None:
        self.response: dict[str, dict[str, list[str]]] = Tools.read_json(TelegramMessages.Error.ERROR)["response"]
        self.SendMessage = Telegram().send_message
    
    def no_slash(self, message: dict[str, str]) -> str | bool:
        chat_id: str = message["chat_id"]
        received_message: str = message["text"]
        
        if isinstance(received_message, str):
            if "/" in received_message:
                self.SendMessage(chat_id, random_msg_from_list(self.response["no_slash"]))
                return False
            return True
        else:
            self.SendMessage(chat_id, random_msg_from_list(self.response["only_text"]))
            return False
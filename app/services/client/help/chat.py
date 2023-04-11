# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   app.services.client.help.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramMessages
from views.client.commands.commands import COMMANDS_LIST, ABOUT_COMMANDS
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list

from typing import Any
#|---------------------------------------------------------------------------------------------------------------------|


class HelpChat(object):
    def __init__(self) -> None:
        self.messages: dict[str, Any] = TelegramMessages.Client.HELP
        self.SendMessage: None = Telegram().send_message
    
    def help_response(self, message: dict[str, Any]) -> None:
        """
        Help message with Ayla Functions
        
        Args:
            message: (dict[str, Any]): Message from Core
        """
        response: dict[str, dict[str, list[str]]] = self.messages["response"]
        chat_id: str = message["chat_id"]
        
        msg_schema: str = random_msg_from_list(response["header"])
        helper_keys: list[str] = [i for i in ABOUT_COMMANDS.keys()]
        
        for key in helper_keys:
            info: list[str] = random_msg_from_list(ABOUT_COMMANDS[key])
            msg_schema += f"{info[0]}{COMMANDS_LIST[key]}{info[1]}"
        
        message_list: list[str] = [
            msg_schema
        ]
        
        for msg in message_list:
            self.SendMessage(chat_id, msg)        
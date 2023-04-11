# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  app.services.client.start.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramMessages
from views.start.commands.commands import COMMANDS_LIST
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list

from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|


class StartChat(object):
    def __init__(self) -> None:
        self.messages: dict[str, Any] = TelegramMessages.Client.START
        self.SendMessage: None = Telegram().send_message
        
    def start_response(self, message: dict[str, Any]) -> None:
        """
        Firsts messages to /start in Telegram

        Args:
            message (dict[str, Any]): Messsage from Core
        """
        response: dict[str, dict[str, list[str]]] = self.messages["response"]
        chat_id: str = message["chat_id"]
        username: str = message["username"]
        
        msg_schema: list[str] = random_msg_from_list(response["hello_again"])
        message_list: list[str] = [
            f"{msg_schema[0]}{username}{msg_schema[1]}{COMMANDS_LIST['help']}{msg_schema[2]}"
        ]
        
        for msg in message_list:
            self.SendMessage(chat_id, msg)
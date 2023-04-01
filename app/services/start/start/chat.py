# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   app.services.start.start.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import Tools, TelegramMessages
from views.start.commands.commands import COMMANDS_LIST
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list

from typing import Any, Union
import json
# |--------------------------------------------------------------------------------------------------------------------|


class StartChat(object):
    def __init__(self) -> None:
        self.messages: dict[str, Any] = Tools.read_json(TelegramMessages.Start.START)
        self.SendMessage: None = Telegram().send_message
        
    def start_response(self, message: dict[str, str]) -> None:
        """
        Firsts messages sended to /start in Telegram

        Args:
            message (dict[str, str]): Message from Core 
        """
        response: dict[str, dict[str, list[Union[str, list]]]] = self.messages["response"]
        chat_id: str = message["chat_id"]
        username: str = message["username"]
        
        # + factor_msg +
        welcome_msg: list[str] = random_msg_from_list(response["welcome"])
        help_msg: list[str] = random_msg_from_list(response['help'])
        
        send_message: list[str] = [
            f"{welcome_msg[0]}{username}{welcome_msg[1]}",
            random_msg_from_list(response["myself"]),
            random_msg_from_list(response["what_do_i_do"]),
            f"{help_msg[0]}{COMMANDS_LIST['help']}{help_msg[1]}"
        ]
        
        for msg in send_message:
            self.SendMessage(chat_id, msg)
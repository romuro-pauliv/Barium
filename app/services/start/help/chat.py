# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    app.services.start.help.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramMessages
from views.start.commands.commands import COMMANDS_LIST, ABOUT_COMMANDS
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list

from typing import Any, Union
import json
# |--------------------------------------------------------------------------------------------------------------------|


class HelpChat(object):
    def __init__(self) -> None:
        self.messages: dict[str, dict[str, Union[str, list[str]]]] = TelegramMessages.Start.HELP
        self.SendMessage: None = Telegram().send_message
    
    def help_response(self, message: dict[str, Any]) -> None:
        """
        Send initial help message

        Args:
            message (dict[str, str]): Message from Core
        """
    
        response: dict[str, dict[str, list[Union[str, list[str]]]]] = self.messages["response"]
        chat_id: str = message["chat_id"]
        
        commands_list_keys: list[str] = [i for i in ABOUT_COMMANDS.keys()]
        msg: str = random_msg_from_list(response["header"])
        
        for keys_ in commands_list_keys:
            help_msg: str = random_msg_from_list(ABOUT_COMMANDS[keys_])
            msg += f"{help_msg[0]}{COMMANDS_LIST[keys_]}{help_msg[1]}"
        
        self.SendMessage(chat_id, msg)
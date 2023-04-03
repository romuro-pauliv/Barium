# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      app.views.start.help.exec_.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from views.start.commands.commands import COMMANDS_LIST
from services.start.help.chat import HelpChat

from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|


class HelpChatExec(object):
    def __init__(self) -> None:
        self.init_command: str = COMMANDS_LIST["help"]
        self.help_chat = HelpChat()
        self.in_execution: list[str] = []
    
    def exec_(self, message: dict[str, Any]) -> None:
        received_message: str = message["text"]
        chat_id: str = message["chat_id"]
        
        if received_message == self.init_command and chat_id not in self.in_execution:
            self.in_execution.append(chat_id)
            self.help_chat.help_response(message)
            self.in_execution.remove(chat_id)
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     app.views.start.start.exec_.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from views.start.commands.commands import COMMANDS_LIST
from services.start.start.chat import StartChat

from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|


class StartChatExec(object):
    def __init__(self) -> None:
        self.init_command: str = COMMANDS_LIST["start"]
        self.start_chat = StartChat()
        self.in_execution: list[str] = []
    
    def exec_(self, message: dict[str, Any]) -> None:
        received_message: str = message["text"]
        chat_id: str = message["chat_id"]

        if received_message == self.init_command and chat_id not in self.in_execution:
            self.in_execution.append(chat_id)
            self.start_chat.start_response(message)
            self.in_execution.remove(chat_id)
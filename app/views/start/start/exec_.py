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
    
    def exec_(self, message: dict[str, Any]) -> None:
        received_message: str = message["text"]
        
        if received_message == self.init_command:
            self.start_chat.start_response(message)
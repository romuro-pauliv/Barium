# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               app.views.client.add_wallet.exec_.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from views.client.commands.commands import COMMANDS_LIST
from services.client.add_wallet.chat import AddWalletChat
from cache.redis_connect import Cache

from typing import Any, Callable
# |--------------------------------------------------------------------------------------------------------------------|


class AddWalletChatExec(object):
    def __init__(self) -> None:
        self.init_command: str = COMMANDS_LIST["add_wallet"]
        self.add_wallet = AddWalletChat()
        self.in_execution: list[str] = []
        
    def exec_(self, message: dict[str, Any]) -> None:
        received_message: str = message["text"]
        chat_id: str = message["chat_id"]
        
        if received_message == self.init_command and chat_id not in self.in_execution:
            self.in_execution.append(chat_id)
            self.add_wallet.open_new_wallet(message)
            self.in_execution.remove(chat_id)
            Cache.TalkMode.add_wallet_branch.mset({chat_id: 0})
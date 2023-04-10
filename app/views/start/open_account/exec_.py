# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                              app.views.start.open_account.exec_.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from views.start.commands.commands import COMMANDS_LIST
from services.start.open_account.chat import OpenAccountChat
from cache.redis_connect import Cache

from typing import Any, Callable, Union
# |--------------------------------------------------------------------------------------------------------------------|


class OpenAccountChatExec(object):
    def __init__(self) -> None:
        self.init_command: str = COMMANDS_LIST["open_account"]
        self.open_account = OpenAccountChat()
        self.in_execution: list[str] = []
    
    def cache_0_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.open_account.wallet_name_valid_and_amount_in_wallet(message)
        chat_id: str = message["chat_id"]
        if response == True:
            Cache.TalkMode.open_account_branch.mset({chat_id: 1})
    
    def cache_1_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.open_account.amount_in_wallet_valid_and_wallet_obs(message)
        chat_id: str = message["chat_id"]
        if response == True:
            Cache.TalkMode.open_account_branch.mset({chat_id: 2})
    
    def cache_2_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.open_account.wallet_obs_valid_and_verify_info(message)
        chat_id: str = message["chat_id"]
        if response == True:
            Cache.TalkMode.open_account_branch.mset({chat_id: 3})
    
    def cache_3_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.open_account.verify_response_and_create_account(message)
    
    def exec_in_cache(self, message: dict[str, Any]) -> None:
        chat_id: str = message["chat_id"]
        
        cache_mode_list: list[Callable[[dict[str, Any]], None]] = [
            self.cache_0_mode,
            self.cache_1_mode,
            self.cache_2_mode,
            self.cache_3_mode
        ]
        
        for n, cache_mode in enumerate(cache_mode_list):
            if int(Cache.TalkMode.open_account_branch.get(chat_id)) == n:
                self.in_execution.append(chat_id)
                cache_mode(message)
                self.in_execution.remove(chat_id)
                break
        
    def exec_(self, message: dict[str, Any]) -> None:
        received_message: str = message["text"]
        chat_id: str = message["chat_id"]
        
        if received_message == self.init_command and chat_id not in self.in_execution:
            self.in_execution.append(chat_id)
            self.open_account.open_first_wallet(message)
            self.in_execution.remove(chat_id)
            Cache.TalkMode.open_account_branch.mset({chat_id: 0})
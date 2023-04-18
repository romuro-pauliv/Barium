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
from log.terminal.cache.redis.methods import RedisCacheLog

from typing import Any, Callable
# |--------------------------------------------------------------------------------------------------------------------|


class AddWalletChatExec(object):
    def __init__(self) -> None:
        self.init_command: str = COMMANDS_LIST["add_wallet"]
        self.add_wallet = AddWalletChat()
        self.in_execution: list[str] = []
    
    def cache_0_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.add_wallet.wallet_name_valid_and_request_amount(message)
        chat_id: str = message["chat_id"]
        if response == True:
            Cache.TalkMode.add_wallet_branch.mset({chat_id: 1}), RedisCacheLog.post(chat_id, "add_wallet_branch")
    
    def cache_1_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.add_wallet.wallet_amount_valid_and_request_obs(message)
        chat_id: str = message["chat_id"]
        if response == True:
            Cache.TalkMode.add_wallet_branch.mset({chat_id: 2}), RedisCacheLog.post(chat_id, "add_wallet_branch")
    
    def cache_2_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.add_wallet.obs_valid_and_request_verify_data(message)
        chat_id: str = message["chat_id"]
        if response == True:
            Cache.TalkMode.add_wallet_branch.mset({chat_id: 3}), RedisCacheLog.post(chat_id, "add_wallet_branch")
    
    def cache_3_mode(self, message: dict[str, Any]) -> None:
        response: bool = self.add_wallet.verify_data_valid_and_conclusion(message)
        chat_id: str = message["chat_id"]
        if response == True:
            Cache.TalkMode.add_wallet_branch.delete(chat_id), RedisCacheLog.delete(chat_id, "add_wallet_branch")
    
    def exec_in_cache(self, message: dict[str, Any]) -> None:
        chat_id: str = message["chat_id"]
        
        cache_mode_list: list[Callable[[dict[str, Any]], None]] = [
            self.cache_0_mode,
            self.cache_1_mode,
            self.cache_2_mode,
            self.cache_3_mode
        ]
        
        for n, cache_mode in enumerate(cache_mode_list):
            if int(Cache.TalkMode.add_wallet_branch.get(chat_id)) == n:
                self.in_execution.append(chat_id)
                cache_mode(message)
                self.in_execution.remove(chat_id)
                break
    
    def exec_(self, message: dict[str, Any]) -> None:
        received_message: str = message["text"]
        chat_id: str = message["chat_id"]
        
        if received_message == self.init_command and chat_id not in self.in_execution:
            self.in_execution.append(chat_id)
            self.add_wallet.open_new_wallet(message)
            self.in_execution.remove(chat_id)
            Cache.TalkMode.add_wallet_branch.mset({chat_id: 0}), RedisCacheLog.post(chat_id, "add_wallet_branch")
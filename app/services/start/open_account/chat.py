# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                            app.services.start.open_account.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramMessages, TelegramConfig
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list
from models.models import TextValidation, ValueValidation, ConditionValidation
from cache.schema.internal_cache import Schema
from cache.redis_connect import Cache
from views.start.commands.commands import COMMANDS_LIST

from log.terminal.cache.internal.methods import InternalCacheLog
from log.terminal.cache.redis.methods import RedisCacheLog
from database.services.open_account import MongoOpenAccount

from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|


class OpenAccountChat(object):
    def __init__(self) -> None:
        self.response: dict[str, Any] = TelegramMessages.Start.OPEN_ACCOUNT["response"]
        self.config_commands: dict[str, Any] = TelegramConfig.COMMANDS["config_commands"]
        self.open_account_command: str = COMMANDS_LIST["open_account"]
        
        self.SendMessage = Telegram().send_message
        
        self.text_validation = TextValidation()
        self.value_validation = ValueValidation()
        self.condition_validation = ConditionValidation()
        
        self.MongoOpenAccount = MongoOpenAccount()
        
        self.cache: dict[str, dict[str, str | float]] = {}
    
    def open_first_wallet(self, message: dict[str, Any]) -> None:
        """
        Send the first message referring to the OpenAccount conversation
        
        Args:
            message (dict[str, Any]): Message from Core
        
        Returns: 
            bool: Boolean response to administrate cache storage
        """
        chat_id: str = message["chat_id"]
        
        send_messages: list[str] = [
            random_msg_from_list(self.response["dialog"]["open_first_wallet"]),
            random_msg_from_list(self.response["quest"]["open_first_wallet"]),
            random_msg_from_list(self.response["info"]["open_first_wallet"])
        ]
        
        for msg in send_messages:
            self.SendMessage(chat_id, msg)
    
    def wallet_name_valid_and_amount_in_wallet(self, message: dict[str, Any]) -> bool:
        """
        Send the message to name the first wallet and valid the wallet name

        Args:
            message (dict[str, str]): Message from Core

        Returns:
            bool: Boolean response to administrate cache storage
        """
        chat_id: str = message["chat_id"]
        received_message: Union[str, list[str, bool]] = message["text"]
        
        if self.text_validation.no_slash(message) == False:
            return False
        
        if self.text_validation.count_character(message) == False:
            return False
        
        self.cache[chat_id] = {Schema.InternalCache.OPEN_ACCOUNT[0]: received_message}
        InternalCacheLog.post(chat_id, "OpenAccountChat", self.cache)
        
        confirmation_msg_schema: list[str] = random_msg_from_list(self.response["confirmation"]["open_first_wallet"])
        
        send_messages: list[str] = [
            f"{confirmation_msg_schema[0]}{received_message}{confirmation_msg_schema[1]}",
            random_msg_from_list(self.response["quest"]["amount_in_first_wallet"])
        ]
        
        for msg in send_messages:
            self.SendMessage(chat_id, msg)
        
        return True
    
    def amount_in_wallet_valid_and_wallet_obs(self, message: dict[str, Any]) -> bool:
        """
        Send the message to request the value wallet and valid the wallet anem

        Args:
            message (dict[str, str]): Message from Core

        Returns:
            bool: Boolean response to admnistrate cache storage
        """
        chat_id: str = message["chat_id"]
        received_message: Union[str, list[str, bool]] = message["text"]
        
        price_validation: dict[str, Union[bool, float]] = self.value_validation.price(chat_id, received_message)
        if price_validation["status"] == False:
            return False
        
        self.cache[chat_id][Schema.InternalCache.OPEN_ACCOUNT[1]] = price_validation["value"]
        InternalCacheLog.post(chat_id, "OpenAccountChat", self.cache)
        
        msg1: str = random_msg_from_list(self.response["confirmation"]["amount_in_first_wallet"])
        
        send_messages: list[str] = [
            f"{msg1[0]}{price_validation['value']}{msg1[1]}",
            random_msg_from_list(self.response["quest"]["wallet_obs"]),
            random_msg_from_list(self.response["info"]["wallet_obs"])
        ]
        
        for msg in send_messages:
            self.SendMessage(chat_id, msg)
        
        return True
    
    def wallet_obs_valid_and_verify_info(self, message: dict[str, Any]) -> bool:
        """
        Wallet obs validation and send a message with wallet info

        Args:
            message (dict[str, str]): Message from Core

        Returns:
            bool: Boolean response to admnistrate cache storage
        """
        
        chat_id: str = message["chat_id"]
        received_message: Union[str, list[str, bool]] = message["text"]
        
        if self.text_validation.no_slash(message) == False:
            return False
        
        if self.text_validation.count_character(message, 100) == False:
            return False
        
        self.cache[chat_id][Schema.InternalCache.OPEN_ACCOUNT[2]] = received_message
        InternalCacheLog.post(chat_id, "OpenAccountChat", self.cache)
        
        msg1: list[str] = random_msg_from_list(self.response["confirmation"]["verify_data"])
        
        msg1_schema: str = f"{msg1[0]}{msg1[1]}{self.cache[chat_id][Schema.InternalCache.OPEN_ACCOUNT[0]]}"\
            f"\n{msg1[2]}{self.cache[chat_id][Schema.InternalCache.OPEN_ACCOUNT[1]]}"\
                f"\n{msg1[3]}{self.cache[chat_id][Schema.InternalCache.OPEN_ACCOUNT[2]]}"
        
        msg2_schema: list[str] = random_msg_from_list(self.response["quest"]["verify_data"])
        
        send_messages: list[str] = [
            msg1_schema,
            f"{msg2_schema[0]}{self.config_commands['yn_response'][0]}{msg2_schema[1]}{self.config_commands['yn_response'][1]}{msg2_schema[2]}"
        ]
        
        for msg in send_messages:
            self.SendMessage(chat_id, msg)
        
        return True
    
    def verify_response_and_create_account(self, message: dict[str, Any]) -> bool:
        chat_id: str = message["chat_id"]
        received_message: Union[str, list[str, bool]] = message["text"]
        
        if self.condition_validation.yn_response(message, self.config_commands["yn_response"]) == False:
            return False
        
        if received_message == self.config_commands["yn_response"][0]:
            self.SendMessage(chat_id, random_msg_from_list(self.response["info"]["yes_conclusion"]))
            
            InternalCacheLog.get(chat_id, "OpenAccountChat", self.cache)
            self.MongoOpenAccount.init_account(message, self.cache[chat_id])

            del self.cache[chat_id]
            InternalCacheLog.delete(chat_id, "OpenAccountChat", self.cache)
            
            Cache.TalkMode.open_account_branch.delete(chat_id), RedisCacheLog.delete(chat_id, "open_account_branch")
            Cache.TalkMode.log_in_branch.mset({chat_id: "active"}), RedisCacheLog.post(chat_id, "log_in_branch")
            
            self.SendMessage(chat_id, random_msg_from_list(self.response["confirmation"]["yes_conclusion"]))
            
            return True
        
        elif received_message == self.config_commands["yn_response"][1]:
            del self.cache[chat_id]
            InternalCacheLog.delete(chat_id, "OpenAccountChat", self.cache)
            
            Cache.TalkMode.open_account_branch.delete(chat_id), RedisCacheLog.delete(chat_id, "open_account_branch")
            
            msg: str = random_msg_from_list(self.response["confirmation"]["no_conclusion"])
            self.SendMessage(chat_id, f"{msg}{self.open_account_command}")
            
            return True
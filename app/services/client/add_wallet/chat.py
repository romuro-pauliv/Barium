# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                             app.services.client.add_wallet.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from core.telegram import Telegram
from config.paths import TelegramMessages
from config.paths import TelegramConfig
from services.tools.tools import random_msg_from_list
from models.models import TextValidation, DatabaseValidation, ValueValidation, ConditionValidation
from cache.schema.internal_cache import Schema
from cache.redis_connect import Cache
from views.client.commands.commands import COMMANDS_LIST
from database.functions.db_func import POST
from log.terminal.cache.internal.methods import InternalCacheLog
from log.terminal.cache.redis.methods import RedisCacheLog
from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|


class AddWalletChat(object):
    def __init__(self) -> None:
        self.SendMessage: None = Telegram().send_message
        self.messages: dict[str, dict] = TelegramMessages.Client.ADD_WALLET

        self.text_validation = TextValidation()
        self.database_validation = DatabaseValidation()
        self.value_validation = ValueValidation()
        self.condition_validation = ConditionValidation()
        
        self.config_commands: list[str] = TelegramConfig.COMMANDS["config_commands"]["yn_response"]
        
        self.cache: dict[str, Any] = {}
        
    def open_new_wallet(self, message: dict[str, Any]) -> None:
        """
        Send messages referring to the Open New Wallet conversation

        Args:
            message (dict[str, Any]): Message from Core
        
        Returns:
            bool: Boolean response to administrate cache storage
        """
        
        chat_id: str = message["chat_id"]
        response: dict[str, list[str]] = self.messages["response"]
        
        msg2_schema: str = random_msg_from_list(response["info"]["open_new_wallet"])
        
        messages_list: list[str] = [
            random_msg_from_list(response["dialog"]["open_new_wallet"]),
            f"{msg2_schema[0]}{COMMANDS_LIST['cancel']}{msg2_schema[1]}",
            random_msg_from_list(response["quest"]["open_new_wallet"])
        ]
        
        for msg in messages_list:
            self.SendMessage(chat_id, msg)
    
    def wallet_name_valid_and_request_amount(self, message: dict[str, Any]) -> bool:
        """
        Send message request to wallet amount and confirm wallet name

        Args:
            message (dict[str, Any]): Message from Core
        
        Returns:
            bool: Boolean response to administrate cache storage
        """
        
        chat_id: str = message["chat_id"]
        response: dict[str, list[str]] = self.messages["response"]
        received_message: str = message["text"]
        
        if self.condition_validation.stop_response(message) == False:
            Cache.TalkMode.add_wallet_branch.delete(chat_id)
            RedisCacheLog.delete(chat_id, 'add_wallet_branch')
            return False
        
        if self.text_validation.no_slash(message) == False:
            return False
        
        if self.text_validation.count_character(message) == False:
            return False
        
        if self.database_validation.wallet_name(message) == False:
            return False
        
        self.cache[chat_id] = {Schema.InternalCache.NEW_WALLET[0]: received_message}
        InternalCacheLog.post(chat_id, "AddWalletChat", self.cache)
        
        msg1_schema: str = random_msg_from_list(response["confirmation"]["open_new_wallet"])
        
        messages_list: list[str] = [
            f"{msg1_schema[0]}{received_message}{msg1_schema[1]}",
            random_msg_from_list(response["quest"]["amount_in_new_wallet"])
        ]
        
        for msg in messages_list:
            self.SendMessage(chat_id, msg)
        
        return True
    
    def wallet_amount_valid_and_request_obs(self, message: dict[str, Any]) -> bool:
        """
        Send message request a obs for wallet and validate the wallet amount

        Args:
            message (dict[str, Any]): Message from Core

        Returns:
            bool: Boolean response to administrate cache storage
        """
        
        chat_id: str = message["chat_id"]
        response: dict[str, list[str]] = self.messages["response"]
        received_message: str = message["text"]
        
        if self.condition_validation.stop_response(message) == False:
            
            Cache.TalkMode.add_wallet_branch.delete(chat_id)
            RedisCacheLog.delete(chat_id, 'add_wallet_branch')
            
            del self.cache[chat_id]
            InternalCacheLog.delete(chat_id, "AddWalletChat", self.cache)
            
            return False
        
        new_value: dict[str, Union[str, float]] = self.value_validation.price(chat_id, received_message)
        if new_value["status"] == False:
            return False
        
        self.cache[chat_id][Schema.InternalCache.NEW_WALLET[1]] = new_value["value"]
        InternalCacheLog.post(chat_id, "AddWalletChat", self.cache)
        
        msg1_schema: str = random_msg_from_list(response["confirmation"]["amount_in_new_wallet"])
        
        messages_list: list[str] = [
            f"{msg1_schema[0]}{str(new_value['value'])}{msg1_schema[1]}",
            random_msg_from_list(response["quest"]["new_wallet_obs"])
        ]
        
        for msg in messages_list:
            self.SendMessage(chat_id, msg)
        
        return True
    
    def obs_valid_and_request_verify_data(self, message: dict[str, Any]) -> bool:
        """
        Send message to user verify the wallet data and validade obs wallet text

        Args:
            message (dict[str, Any]): Message from Core

        Returns:
            bool: Boolean response to administrate cache storage
        """
        
        chat_id: str = message["chat_id"]
        response: dict[str, list[str]] = self.messages["response"]
        received_message: str = message["text"]
        
        if self.condition_validation.stop_response(message) == False:
            
            Cache.TalkMode.add_wallet_branch.delete(chat_id)
            RedisCacheLog.delete(chat_id, 'add_wallet_branch')
            
            del self.cache[chat_id]
            InternalCacheLog.delete(chat_id, "AddWalletChat", self.cache)
            return False
        
        if self.text_validation.count_character(message, 100) == False:
            return False
        
        self.cache[chat_id][Schema.InternalCache.NEW_WALLET[2]] = received_message
        InternalCacheLog.post(chat_id, "AddWalletChat", self.cache)
        
        msg1_schema: list[str] = random_msg_from_list(response["confirmation"]["verify_data"])
        msg1: str = f"{msg1_schema[0]}{msg1_schema[1]}{self.cache[chat_id][Schema.InternalCache.NEW_WALLET[0]]}\n"
        msg1 += f"{msg1_schema[2]}{self.cache[chat_id][Schema.InternalCache.NEW_WALLET[1]]}\n"
        msg1 += f"{msg1_schema[3]}{self.cache[chat_id][Schema.InternalCache.NEW_WALLET[2]]}"
        
        msg2_schema: list[str] = random_msg_from_list(response["quest"]["verify_data"])
        msg2: str = f"{msg2_schema[0]}{self.config_commands[0]}{msg2_schema[1]}{self.config_commands[1]}{msg2_schema[2]}"
        
        send_messages: list[str] = [
            msg1,
            msg2
        ]
        
        for msg in send_messages:
            self.SendMessage(chat_id, msg)
        
        return True

    def verify_data_valid_and_conclusion(self, message: dict[str, Any]) -> bool:
        """
        Verify /yes or /no response and confirm new wallet
        Args:
            message (dict[str, Any]): Message from Core

        Returns:
            bool: Boolean response to administrate cache storage
        """
        
        chat_id: str = message["chat_id"]
        response: dict[str, list[str]] = self.messages["response"]
        username: str = message["username"]
        received_message: str = message["text"]
        
        
        if self.condition_validation.yn_response(message, self.config_commands) == False:
            return False
        
        if received_message == self.config_commands[0]:
            self.SendMessage(chat_id, random_msg_from_list(response["info"]["yes_conclusion"]))
            
            POST.add_wallet(chat_id, username, self.cache[chat_id])
            
            del self.cache[chat_id]
            InternalCacheLog.delete(chat_id, "AddWalletChat", self.cache)
            
            self.SendMessage(chat_id, random_msg_from_list(response["confirmation"]["yes_conclusion"]))
            return True
        
        elif received_message == self.config_commands[1]:
            
            del self.cache[chat_id]
            InternalCacheLog.delete(chat_id, "AddWalletChat", self.cache)
            
            msg1: str = random_msg_from_list(response["confirmation"]["no_conclusion"])
            self.SendMessage(chat_id, f"{msg1}{COMMANDS_LIST['add_wallet']}")
            return True
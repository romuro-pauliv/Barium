# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                            app.services.start.open_account.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import Tools, TelegramMessages
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list
from models.models import TextValidation, ValueValidation
from cache.schema.internal_cache import Schema

from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|


class OpenAccountChat(object):
    def __init__(self) -> None:
        self.response: dict[str, Any] = Tools.read_json(TelegramMessages.Start.OPEN_ACCOUNT)["response"]
        self.SendMessage = Telegram().send_message
        
        self.text_validation = TextValidation()
        self.value_validation = ValueValidation()
        
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
        
        confirmation_msg_schema: list[str] = random_msg_from_list(self.response["confirmation"]["open_first_wallet"])
        
        send_messages: list[str] = [
            f"{confirmation_msg_schema[0]}{received_message}{confirmation_msg_schema[1]}",
            self.response["quest"]["amount_in_first_wallet"]
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
        
        send_messages: list[str] = [
            random_msg_from_list(self.response["confirmation"]["amount_in_first_wallet"]),
            random_msg_from_list(self.response["quest"]["wallet_obs"])
        ]
        
        for msg in send_messages:
            self.SendMessage(chat_id, msg)
        
        return True
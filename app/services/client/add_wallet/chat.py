# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                             app.services.client.add_wallet.chat.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from core.telegram import Telegram
from config.paths import TelegramMessages
from services.tools.tools import random_msg_from_list
from models.models import TextValidation


from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|


class AddWalletChat(object):
    def __init__(self) -> None:
        self.SendMessage: None = Telegram().send_message
        self.messages: dict[str, dict] = TelegramMessages.Client.ADD_WALLET

        self.text_validation = TextValidation()
        
        self.wallet_name_cache: dict[str, Any] = {}
        
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
        
        messages_list: list[str] = [
            random_msg_from_list(response["dialog"]["open_new_wallet"]),
            random_msg_from_list(response["info"]["open_new_wallet"]),
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
        
        if self.text_validation.count_character(message) == False:
            return False
        
        self.SendMessage(chat_id, "testing")
        return True
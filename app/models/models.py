# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               app.models.models.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramMessages
from core.telegram import Telegram
from services.tools.tools import random_msg_from_list
from database.functions.db_func import GET

from string import digits
from typing import Union, Any
# |--------------------------------------------------------------------------------------------------------------------|


class TextValidation(object):
    def __init__(self) -> None:
        self.response: dict[str, dict[str, list[str]]] = TelegramMessages.Error.ERROR["response"]
        self.SendMessage = Telegram().send_message
    
    def no_slash(self, message: dict[str, str]) -> bool:
        chat_id: str = message["chat_id"]
        received_message: str = message["text"]
        
        if isinstance(received_message, str):
            if "/" in received_message:
                self.SendMessage(chat_id, random_msg_from_list(self.response["no_slash"]))
                return False
            return True
        else:
            self.SendMessage(chat_id, random_msg_from_list(self.response["only_text"]))
            return False
    
    def count_character(self, message: dict[str, str], n_char: int = 30) -> bool:
        chat_id: str = message["chat_id"]
        received_message: str = message["text"]
        
        if isinstance(received_message, str):
            if len(received_message) > n_char:
                self.SendMessage(chat_id, random_msg_from_list(self.response["count_character"]))
                return False
            return True
        else:
            self.SendMessage(chat_id, random_msg_from_list(self.response["only_text"]))
            return False
    

class ConditionValidation(object):
    def __init__(self) -> None:
        self.response: dict[str, dict[str, list[str]]] = TelegramMessages.Error.ERROR["response"]
        self.SendMessage = Telegram().send_message
    
    def yn_response(self, message: dict[str, Any], two_commands: list[str, str]) -> bool:
        chat_id: str = message["chat_id"]
        received_message: str = message["text"]
        
        if isinstance(received_message, str):
            if received_message in two_commands:
                return True
            else:
                msg_schema: list[str] = self.response["yn_response"]
                msg: str = f"{msg_schema[0]}{two_commands[0]}{msg_schema[1]}{two_commands[1]}{msg_schema[2]}"
                self.SendMessage(chat_id, msg)
                return False
        else:
            self.SendMessage(chat_id, random_msg_from_list(self.response["only_text"]))
            return False
    

class ValueValidation(object):
    def __init__(self) -> None:
        self.response: dict[str, dict[str, list[str]]] = TelegramMessages.Error.ERROR["response"]
        self.SendMessage = Telegram().send_message
        
    def price(self, chat_id: str, value: str) -> dict[str, Union[str, float]]:   
        if not isinstance(value, str):
            self.SendMessage(chat_id, random_msg_from_list(self.response["only_text"]))
            return {"status": False}
        
        new_value: str = ""
        add_characters: str = ".,-"
        char_status: dict[str, dict[str, int]] = {
            "amount": {
                "dot": 0,
                "bar": 0,
                "number": 0
            },
            "max_amount": {
                "dot": 1,
                "bar": 1,
                "number": 17
            },
            "min_amount": {
                "dot": 0,
                "bar": 0,
                "number": 1
            }
        }
        
        for char_ in value:
            
            response: dict[str, list[str]] = self.response["only_price"]
            response_key: list[str] = ["many_numbers", "many_punct", "many_punct"]
            char_mode: list[str] = ["number", "dot", "bar"]
            char_verification: list[str] = [digits, ",.", "-"]
            new_value_input: list[str] = [None, ".", "-"]
            
            if char_ not in str(digits + add_characters):
                self.SendMessage(chat_id, random_msg_from_list(self.response["only_price"]["forbidden_character"]))
                return {"status": False}
            
            for n, key in enumerate(response_key):
                if char_ in char_verification[n]:
                    char_status["amount"][char_mode[n]] += 1
                    if char_status["amount"][char_mode[n]] > char_status["max_amount"][char_mode[n]]:
                        self.SendMessage(chat_id, random_msg_from_list(response[key]))
                        return {"status": False}
                    
                    if n == 0:
                        new_value += char_
                    else:
                        new_value += new_value_input[n]
            
            
        for keys in char_status["amount"].keys():
            if char_status["amount"][keys] < char_status["min_amount"][keys]:
                self.SendMessage(chat_id, random_msg_from_list(self.response["only_price"]["missing_info"]))
                return {"status": False}
        
        if char_status["amount"]["bar"] != 0 and new_value[0] != "-":
            self.SendMessage(chat_id, random_msg_from_list(self.response["only_price"]["negative_value"]))
            return {"status": False}
        
        if char_status["amount"]["dot"] != 0:
            terms: list[str] = new_value.split(".")
            if len(terms[1]) > 2:
                self.SendMessage(chat_id, random_msg_from_list(self.response["only_price"]["many_decimals"]))
                return {"status": False}
        
        return {"status": True, "value": float(new_value)}


class DatabaseValidation(object):
    def __init__(self) -> None:
        self.response: dict[str, dict[str, list[str]]] = TelegramMessages.Error.ERROR["response"]
        self.SendMessage = Telegram().send_message
    
    def wallet_name(self, message: dict[str, str]) -> bool:
        chat_id: str = message["chat_id"]
        received_message: str = message["text"]
        
        if received_message in GET.wallet_list(chat_id):
            self.SendMessage(chat_id, random_msg_from_list(self.response["forbidden_wallet_name"]))
            return False
        return True
        
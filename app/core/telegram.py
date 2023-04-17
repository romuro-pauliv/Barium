# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               app.core.telegram.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import TelegramConfig
from core.tools.threading_mode import run_in_background

from log.terminal.messages import MessagesLog


from dotenv import load_dotenv
load_dotenv()

from typing import Any, Union
import requests
import os
# |--------------------------------------------------------------------------------------------------------------------|


class Telegram(object):
    def __init__(self) -> None:
        data: dict[str, Any] = TelegramConfig.API
        
        self.api: str = f"{data['uri']}{os.getenv('TOKEN')}"
        self.endpoint: dict[str, str] = data["endpoint"]
        
        self.update_id: int = 0
        self.cache: dict[str, Any] = {"last_message": {}}
    
    def request(self, API_method: str, HTTP_method: str, params: dict[str, Any] = None) -> dict[str, Any]:
        """
        Makes a request to the Telegram Bot API using the given API method and HTTP method.
        It takes two arguments:
        Args:
            API_method (str): A string representing the API method to be used in the request.
            HTTP_method (str): a string representing the HTTP method to be used in the request.

        Returns:
            dict[str, Any]: The function returns a dictionary containing the response from the API.
        """
        response: requests.models.Response = eval(f"requests.{HTTP_method}('{self.api}{API_method}', params={params})")
        return response.json()
    
    def send_message(self, chat_id: str, message: str) -> None:
        """
        Send a text message to client for chat_id
        Args:
            chat_id (str): talk chat_id
            message (str): sended message
        """
        params: dict[str, str] = {"chat_id": chat_id, "text": message, "parse_mode": "html"}
        
        run_in_background(MessagesLog.send_message, (chat_id, message,))
        
        try:
            self.request(self.endpoint['send_message'], "post", params)
        except requests.exceptions.ConnectionError:
            pass
    
    def last_message(self) -> Union[dict[str, str], None]:
        """
        The last_message method of the Telegram class retrieves the latest message from a Telegram chat using the 
        Telegram Bot API.
        Returns:
            Union[dict[str, str], None]: If there are new messages, returns a dictionary containing the information of 
            the new messages in the format
        """
        updates: dict[str, Any] = self.request(
            self.endpoint["updates"], "get", params={"offset": self.update_id})["result"]

        chats_ids: list[str] = []
        last_msg: dict[str, str] = {}
        new_messages: dict[str, str] = {}
            
        for update in updates:
            self.update_id: int = int(update["update_id"])
            if "message" in [keys for keys in update.keys()]:
                data: dict[str, str] = update["message"]

                chat_id: str = data["chat"]["id"]
                username: str = data["chat"]["first_name"]
                date: str = data["date"]
                try:
                    text: str = data["text"]
                except KeyError:
                    text: list[str, bool] = ["BIN", bool]
            
                if chat_id in chats_ids:
                    if last_msg[chat_id]["date"] < date:
                        last_msg[chat_id] = {"username": username, "date": date, "text": text}
                else:
                    chats_ids.append(chat_id)
                    last_msg[chat_id] = {"username": username, "date": date, "text": text}
        
        
        chat_id_in_cache: list[str] = [_id for _id in last_msg.keys()]
        for _id in chat_id_in_cache:
            try:
                old_message: dict[str, str] = self.cache["last_message"][_id]
                if old_message != last_msg[_id] and old_message["date"] < last_msg[_id]["date"]:
                    self.cache["last_message"][_id] = last_msg[_id]
                    new_messages[_id] = last_msg[_id]
                    
            except KeyError:
                self.cache["last_message"][_id] = last_msg[_id]
                new_messages[_id] = last_msg[_id]
        
        return new_messages if new_messages else None
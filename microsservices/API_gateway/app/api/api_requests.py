# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                api.api_requests.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Any

from config.paths import TelegramConfig

import os
import requests
from dotenv import load_dotenv
load_dotenv()
# |--------------------------------------------------------------------------------------------------------------------|


class TelegramApiRequest(object):
    def __init__(self) -> None:
        self.api_data: dict[str, Any] = TelegramConfig.TELEGRAM_API_DATA
        self.uri: str = f"{self.api_data['uri']}{os.getenv('TOKEN')}"
    
    def api_request(self, API_method: str, HTTP_method: str, params: dict[str, Any] = None) -> dict[str, Any]:
        """
        Makes a request to the Telegram API using the given API method and HTTP method.
        It takes two arguments:
        Args:
            API_method (str): A string representing the API method to be used in the request
            HTTP_method (str): A string representing the HTTP method to be used in the request
        Returns:
            dict[str, Any]: The function returns a dictionary containing the response from the API
        """
        
        response: requests.models.Response = eval(f"requests.{HTTP_method}('{self.uri}{API_method}', params={params})")
        return response.json()
    
    def send_message(self, chat_id: str, message: str) -> None:
        """
        Send a text message to client for chat_id
        Args:
            chat_id (str): talk chat_id
            message (str): sended message
        """
        params: dict[str, str] = {"chat_id": chat_id, "text": message, "parse_mode": "html"}
        try:
            self.api_request("/sendMessage", "post", params)
        except requests.exceptions.ConnectionError:
            pass
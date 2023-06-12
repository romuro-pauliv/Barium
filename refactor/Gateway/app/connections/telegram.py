# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        app.connections.telegram.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Any, Union

from dotenv import load_dotenv
import requests
import os

from resources.data import TELEGRAM_API
# |--------------------------------------------------------------------------------------------------------------------|

load_dotenv()

class TelegramRequests(object):
    def __init__(self) -> None:
        """
        Initialize the TelegramRequests instance.
        """
        self.route: dict[str, Any] = TELEGRAM_API
        self.uri: str = f"{self.route['uri']}{os.getenv('TOKEN')}"
        
    def make_request(self, method_: str, endpoint: str, params: dict[str, Any] = None) -> Union[dict[str, Any], None]:
        """
        Make a request to the Telegram API.
        Args:
            method_ (str): HTTP method (e.g., "GET", "POST").
            endpoint (str): API endpoint.
            params (dict[str, Any], optional): Request parameters. Defaults to None.
        Returns:
            dict[str, Any]: JSON response from the API.
        """
        try:
            response: requests.models.Response = requests.request(method_, f"{self.uri}{endpoint}", params=params)
            return response.json()
        except requests.exceptions.HTTPError as errh:
            pass
        except requests.exceptions.ProxyError as errp:
            pass
        except requests.exceptions.ConnectionError as errc:
            pass
        except requests.exceptions.Timeout as errt:
            pass
        except requests.exceptions.RequestException as err:
            pass
    
    def send_message(self, chat_id: str, message: str) -> None:
        """
        Send a message via the Telegram API.
        Args:
            chat_id (str): ID of the chat to send the message to.
            message (str): Content of the message.
        """
        params: dict[str, str] = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "html"
        }
        self.make_request("post", self.route['endpoints']['send_message'], params)
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        api.connections.telegram.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Any, Union

from dotenv import load_dotenv
import requests
import os

from api.resources.data import TELEGRAM_API

from api.connections.log import LogConnect
# |--------------------------------------------------------------------------------------------------------------------|

load_dotenv()
log_connect: LogConnect = LogConnect()


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
        uri_to_log: str = f"{self.route['uri']}[token]{endpoint}"
        try:
            response: requests.models.Response = requests.request(method_, f"{self.uri}{endpoint}", params=params)
            return response.json()
        except requests.exceptions.HTTPError as errh:
            log_connect.report(method_, uri_to_log, "error", "INTERNAL", False, "HTTP Error")
            pass
        except requests.exceptions.ProxyError as errp:
            log_connect.report(method_, uri_to_log, "error", "INTERNAL", False, "Proxy Error")
            pass
        except requests.exceptions.ConnectionError as errc:
            log_connect.report(method_, uri_to_log, "error", "INTERNAL", False, "Error Connecting")
            pass
        except requests.exceptions.Timeout as errt:
            log_connect.report(method_, uri_to_log, "error", "INTERNAL", False, "Timeout Error")
            pass
        except requests.exceptions.RequestException as err:
            log_connect.report(method_, uri_to_log, "error", "INTERNAL", False, "Unknown Error")
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
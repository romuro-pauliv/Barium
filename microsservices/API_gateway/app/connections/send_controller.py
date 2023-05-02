# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 app.connections.send_controller.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from errors.send_to_telegram import system_down_message
from config.paths import MicrosservicesAPI

from typing import Any
import requests
import threading
# |--------------------------------------------------------------------------------------------------------------------|

class SendToController(object):
    def __init__(self) -> None:
        self.host: str = MicrosservicesAPI.CONTROLLER_ROUTE["controller"]["HOST"]
        self.port: str = MicrosservicesAPI.CONTROLLER_ROUTE["controller"]["PORT"]
        self.dir: str = MicrosservicesAPI.CONTROLLER_ROUTE["controller"]["DIR"]
    
    def post(self, message_data: dict[str, Any]) -> None:
        try:
            requests.post(f"{self.host}:{self.port}{self.dir}", json=message_data)
        except requests.exceptions.ConnectionError:
            system_down_message(message_data["chat_id"])
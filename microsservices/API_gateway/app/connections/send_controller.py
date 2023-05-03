# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 app.connections.send_controller.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from errors.send_to_telegram import system_down_message
from config.paths import MicrosservicesAPI
from connections.send_log import SendToLog
from config.paths import LogSchema

from typing import Any
import requests
# |--------------------------------------------------------------------------------------------------------------------|

class SendToController(object):
    def __init__(self) -> None:
        self.host: str = MicrosservicesAPI.MS_ROUTES["controller"]["HOST"]
        self.port: str = MicrosservicesAPI.MS_ROUTES["controller"]["PORT"]
        self.dir: str = MicrosservicesAPI.MS_ROUTES["controller"]["DIR"]
    
    def post(self, message_data: dict[str, Any]) -> None:
        try:
            requests.post(f"{self.host}:{self.port}{self.dir}", json=message_data)
        except requests.exceptions.ConnectionError:
            system_down_message(message_data["chat_id"])
            log_schema: list[str] = LogSchema.LOG_REPORT_MSG["controller"]["no_connection"]
            SendToLog().report(log_schema[0], log_schema[1], message_data["chat_id"])
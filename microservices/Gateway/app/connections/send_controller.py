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
        """
        Loading Controller route data to use in self.post
        """
        controller_route_data: dict[str, str] = MicrosservicesAPI.MS_ROUTES["controller"]
        self.host: str = controller_route_data["HOST"]
        self.port: str = controller_route_data["PORT"]
        self.path1: str = controller_route_data["PATH1"]
        self.endpoint: str = controller_route_data["ENDPOINTS"]["home"]
    
    def log_report(self, master: str, log_data: str, message_data: str) -> None:
        """
        Resume log message loading and send to LOG microservice
        Args:
            master (str): Higher key in LOG_REPORT_MSG .json
            log_data (str): lower key (log message data) in LOG_REPORT_MSG .json
            message_data (str): Handled message from Telegram API
        """
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
        SendToLog().report(log_schema[0], log_schema[1], message_data["chat_id"])
    
    def post(self, message_data: dict[str, Any]) -> None:
        """
        Send message data to Controller Microservice
        Args:
            message_data (dict[str, Any]): Handled message from Telegram API
        """
        try:
            self.log_report("controller", "sent_to_controller", message_data)
            requests.post(f"{self.host}:{self.port}{self.path1}{self.endpoint}", json=message_data)
        except requests.exceptions.ConnectionError:
            system_down_message(message_data["chat_id"])
            self.log_report("controller", "no_connection", message_data)
            self.log_report("telegram_api", "error_message", message_data)
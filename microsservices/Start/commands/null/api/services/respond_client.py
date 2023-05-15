# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     api.services.respond_client.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.services.tools.random_msg_from_list import random_msg_from_list
from api.config.paths import Messages, LogSchema, MicrosservicesAPI
from api.connections.send_log import SendToLog
from api.errors.send_to_telegram import system_down_message

import threading
import requests
# |--------------------------------------------------------------------------------------------------------------------|


class RespondClient(object):
    def __init__(self) -> None:
        self.msg_list: list[str] = Messages.MESSAGES["null"]
        self.sender_route_data: dict[str, str] = MicrosservicesAPI.MS_ROUTES["sender"]
        
        self.HOST: str = self.sender_route_data["HOST"]
        self.PORT: str = self.sender_route_data["PORT"]
        self.DIR: str = self.sender_route_data["DIR"]
    
    def log_report(self, master: str, log_data: str, chat_id: str) -> None:
        self.log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
        
        threading.Thread(
            target=SendToLog().report,
            args=(self.log_schema[0], self.log_schema[1], chat_id)
        ).start()
    
    def post(self, message: dict[str, str | list]) -> None:
        msg_to_send: dict[str] = {
            "chat_id": message["chat_id"],
            "message": random_msg_from_list(self.msg_list)
        }
        
        try:
            requests.post(f"{self.HOST}:{self.PORT}{self.DIR}", json=msg_to_send)
            self.log_report("connections", "sent_completed", message["chat_id"])
        except requests.exceptions.ConnectionError:
            self.log_report("connections", "sent_failed", message["chat_id"])
            system_down_message(message["chat_id"])
            self.log_report("telegram_api", "error_message", message["chat_id"])
        
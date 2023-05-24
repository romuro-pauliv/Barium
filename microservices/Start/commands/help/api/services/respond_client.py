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
        self.msg_list: list[str] = Messages.MESSAGES["help"]
        self.sender_route_data: dict[str, str] = MicrosservicesAPI.MS_ROUTES["sender"]
        self.whoami: dict[str, str] = MicrosservicesAPI.WHO_AM_I
        
        self.HOST: str = self.sender_route_data["HOST"]
        self.PORT: str = self.sender_route_data["PORT"]
        self.PATH: str = self.sender_route_data["PATH1"]["path"]
        self.ENDPOINT: str = self.sender_route_data["PATH1"]["endpoints"]["home"]
    
    def log_report(self, master: str, log_data: str, chat_id: str) -> None:
        """
        Send a report to LOG MS
        Args:
            master (str): Upper key from log_report.json
            log_data (str): Lower key from log_report.json
            chat_id (str): chat_id received message
        """
        self.log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
        
        threading.Thread(
            target=SendToLog().report,
            args=(self.log_schema[0], self.log_schema[1], chat_id)
        ).start()
        
    def post(self, message: dict[str, str | list]) -> None:
        """
        Send a client message to Sender MS
        Args:
            message (dict[str, str  |  list]): Received message with chat_id
        """
        
        if "cache" in [i for i in message.keys()]:
            pass
        else:
            random_msg: str = random_msg_from_list(self.msg_list)
            msg_to_send: dict[str] = {
                "chat_id": message["chat_id"],
                "message": random_msg,
                "microservice": [self.whoami["NAME"], str(self.whoami["HOST"] + ":" + self.whoami["PORT"])]
            }
            
            try:
                requests.post(f"{self.HOST}:{self.PORT}{self.PATH}{self.ENDPOINT}", json=msg_to_send)
                self.log_report("connections", "sent_completed", message["chat_id"])
            except requests.exceptions.ConnectionError:
                self.log_report("connections", "sent_failed", message["chat_id"])
                system_down_message(message["chat_id"])
                self.log_report("telegram_api", "error_message", message["chat_id"])
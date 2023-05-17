# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        app.connections.send_log.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from config.paths import MicrosservicesAPI

from typing import AnyStr
import requests
# |--------------------------------------------------------------------------------------------------------------------|


class SendToLog(object):
    def __init__(self) -> None:
        """
        Loading Log route data to use with Log microservice
        """
        self.log_route_data: dict[str, str] = MicrosservicesAPI.MS_ROUTES["logs"]
        self.host: str = self.log_route_data["HOST"]
        self.port: str = self.log_route_data["PORT"]
        self.dir: str = self.log_route_data["DIR"]
        
    def report(self, REPORT: str, LOG_LEVEL: str, chat_id: str) -> None:
        """
        Send a report to Log microservice
        Args:
            REPORT (str): Log information
            LOG_LEVEL (str): Log level ["debug", "info", "warning", "error", "critical"]
            chat_id (str): chat_id generator of the log report or "INTERNAL" to internal exceptions
        """
        send_json: dict[str] = {
            "report": REPORT,
            "extra": {"microservice": "GATEWAY", "clientip": "LOCAL", "chat_id": chat_id}
        }
        
        debug_endpoint: str = self.log_route_data["ENDPOINTS"][LOG_LEVEL]
        request_uri: str = f"{self.host}:{self.port}{self.dir}{debug_endpoint}"
        
        try:
            requests.post(request_uri, json=send_json)
        except requests.exceptions.ConnectionError:
                pass
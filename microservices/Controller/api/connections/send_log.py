# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        app.connections.send_log.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.config.paths import MicrosservicesAPI
import requests
# |--------------------------------------------------------------------------------------------------------------------|


class SendToLog(object):
    def __init__(self) -> None:
        """
        Loading Log route data to use with Log microservice
        """
        self.who_am_i: dict[str, str] = MicrosservicesAPI.WHO_AM_I
        self.log_route_data: dict[str, str] = MicrosservicesAPI.MS_ROUTES["logs"]
        self.host: str = self.log_route_data["HOST"]
        self.port: str = self.log_route_data["PORT"]
        self.path1: str = self.log_route_data["PATH1"]
        
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
            "extra": {
                "microservice": self.who_am_i["NAME"],
                "clientip": str(self.who_am_i["HOST"] + ":" + self.who_am_i["PORT"]),
                "chat_id": chat_id}
        }
        
        debug_endpoint: str = self.log_route_data["ENDPOINTS"][LOG_LEVEL]
        request_uri: str = f"{self.host}:{self.port}{self.path1}{debug_endpoint}"
        
        try:
            requests.post(request_uri, json=send_json)
        except requests.exceptions.ConnectionError:
                pass
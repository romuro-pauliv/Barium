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
        self.host: str = MicrosservicesAPI.MS_ROUTES["logs"]["HOST"]
        self.port: str = MicrosservicesAPI.MS_ROUTES["logs"]["PORT"]
        self.dir: str = MicrosservicesAPI.MS_ROUTES["logs"]["DIR"]
        
    def report(self, REPORT: str, LOG_LEVEL: str, chat_id: str) -> None:
        """
        Send to MS LOG a report
        Args:
            REPORT (str): Log information
            LOG_LEVEL (str): Log level ["debug", "info", "warning", "error", "critical"]
            chat_id (str): chat_id generator of the log report
        """
        send_json: dict[str] = {
            "report": REPORT,
            "extra": {"microservice": "DATALOADING", "clientip": "127.0.0.1:5002", "chat_id": chat_id}
        }
        
        debug_endpoint: str = MicrosservicesAPI.MS_ROUTES["logs"]["ENDPOINTS"][LOG_LEVEL]
        request_uri: str = f"{self.host}:{self.port}{self.dir}{debug_endpoint}"
        
        try:
            requests.post(request_uri, json=send_json)
        except requests.exceptions.ConnectionError:
                pass
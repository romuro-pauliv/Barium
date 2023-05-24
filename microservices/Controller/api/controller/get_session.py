# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      api.controller.get_session.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from api.config.paths import MicrosservicesAPI

from api.connections.send_log import SendToLog
from api.config.paths import LogSchema

import threading
# |--------------------------------------------------------------------------------------------------------------------|


class Session(object):
    def __init__(self) -> None:
        """
        Loading data loading route data microservice and read log_report from .json
        """
        data_loading_route: dict[str, str] = MicrosservicesAPI.MS_ROUTES["data_loading"]
        
        self.HOST: str = data_loading_route["HOST"]
        self.PORT: str = data_loading_route["PORT"]
        self.PATH: str = data_loading_route["PATH1"]["path"]
        self.ENDPOINT: str = data_loading_route["PATH1"]['endpoints']["home"]
        
        self.sessions: list[str] = []
        
        self.failed: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["get_session_failed"]
        self.completed: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["get_session_completed"]
        self.send_to_log: SendToLog = SendToLog()
    
    def log_thread(self, log_schema: list[str]) -> None:
        """
        Send a log report to Log Microservice in another thread
        Args:
            log_schema (list[str]): List content a log report, log level, and ID
        """
        threading.Thread(
            target=self.send_to_log.report, args=(
                log_schema[0], log_schema[1], log_schema[2]
            )
        ).start()
                
    def request(self) -> bool:
        """
        Request session from Data Loading Microservice

        Returns:
            bool: True if return correctly
        """
        try:
            response: requests.models.Response = requests.get(f"{self.HOST}:{self.PORT}{self.PATH}{self.ENDPOINT}")
        except requests.exceptions.ConnectionError:
            self.log_thread(self.failed)
            return False
            
        if response.status_code == 200:
            self.log_thread(self.completed)
            self.sessions = response.json()
            return True
        else:
            self.log_thread(self.failed)
            return False
    
    def get(self) -> list[str]:
        """
        Get session. Must be executed after a request function. Also, the return it will be [] (a empty list)
        Returns:
            list[str]: return clients session's
        """
        return self.sessions
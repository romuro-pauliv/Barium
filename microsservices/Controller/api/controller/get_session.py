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
        data_loading_route: dict[str, str] = MicrosservicesAPI.MS_ROUTES["data_loading"]
        self.HOST: str = data_loading_route["HOST"]
        self.PORT: str = data_loading_route["PORT"]
        self.DIR: str = data_loading_route["DIR"]
        self.sessions: list[str] = []
        
        self.failed: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["get_session_failed"]
        self.completed: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["get_session_completed"]
        self.send_to_log: SendToLog = SendToLog()
    
    def log_thread(self, log_schema: list[str]) -> None:
        threading.Thread(
            target=self.send_to_log.report, args=(
                log_schema[0], log_schema[1], log_schema[2]
            )
        ).start()
                
    def request(self) -> bool:
        try:
            response: requests.models.Response = requests.get(f"{self.HOST}:{self.PORT}{self.DIR}")
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
        return self.sessions
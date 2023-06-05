# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       api.services.request_data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.send_log import SendToLog
from api.config.paths import LogSchema, MicrosservicesAPI, Messages

from api.connections.sender import connect_with_sender
from api.connections.data_loading import DataLoading

from api.services.tools.random_msg_from_list import random_msg_from_list

import threading
import time
# |--------------------------------------------------------------------------------------------------------------------|


class RequestUserData(object):
    def __init__(self) -> None:
        pass    
    
    def log_report(self, master: str, log_data: str, chat_id: str) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
        threading.Thread(
            target=SendToLog().report,
            args=(log_schema[0], log_schema[1], chat_id)
        ).start()
        
    def send(self, chat_id: str) -> None:
        self.whoami: dict[str, str] = MicrosservicesAPI.WHO_AM_I
        message_keys: list[str] = ["sherlock", "request_username"]
        
        # Input in Cache |---------------------------------------------------------------------------------------------|
        if DataLoading.send_cache(
            route=MicrosservicesAPI.MS_ROUTES["data_loading"],
            post_json={"chat_id": chat_id, "cache_value": "SHERLOCK_0"},
            chat_id=chat_id,
            log_report_function=self.log_report
        ) == True:
        # |------------------------------------------------------------------------------------------------------------|
            
            for msg_key in message_keys:
                connect_with_sender(
                    route=MicrosservicesAPI.MS_ROUTES["sender"],
                    post_json={
                        "chat_id": chat_id,
                        "message": random_msg_from_list(Messages.MESSAGES[msg_key]),
                        "microservice": [self.whoami["NAME"], str(self.whoami["HOST"] + ":" + self.whoami["PORT"])]
                    },
                    chat_id=chat_id,
                    log_report_function=self.log_report
                )
                time.sleep(0.5)
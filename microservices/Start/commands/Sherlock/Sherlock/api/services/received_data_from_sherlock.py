# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                        api.services.received_data_from_sherlock.py |
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


class ReceivedDataSherlock(object):
    def __init__(self) -> None:
        pass
    
    def log_report(self, master: str, log_data: str, chat_id: str) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
        threading.Thread(
            target=SendToLog().report,
            args=(log_schema[0], log_schema[1], chat_id)
        ).start()
    
    def finish_msg(self, data: dict[str, str]) -> None:
        self.whoami: dict[str, str] = MicrosservicesAPI.WHO_AM_I
                
        if data["site"] == False and data["uri"] == False:
            if DataLoading.delete_cache(
                route=MicrosservicesAPI.MS_ROUTES["data_loading"],
                post_json={"chat_id": data["chat_id"]},
                chat_id=data["chat_id"],
                log_report_function=self.log_report
              ) == True:
                
                connect_with_sender(
                    route=MicrosservicesAPI.MS_ROUTES["sender"],
                    post_json={
                        "chat_id": data["chat_id"],
                        "message": Messages.MESSAGES["finish_completed"],
                        "microservice": [self.whoami["NAME"], str(self.whoami["HOST"] + ":" + self.whoami["PORT"])]
                    },
                    chat_id=data["chat_id"],
                    log_report_function=self.log_report
                )
                return True
        return False
        
    def send(self, data: dict[str, str]) -> None:
        
        if self.finish_msg(data) == False:
        
            self.whoami: dict[str, str] = MicrosservicesAPI.WHO_AM_I
            msg: str = str("🌐 " + data["site"] + "\n" + "🔗 "+ data["uri"])
        
            connect_with_sender(
                route=MicrosservicesAPI.MS_ROUTES["sender"],
                post_json={
                    "chat_id": data["chat_id"],
                    "message": msg,
                    "microservice": [self.whoami["NAME"], str(self.whoami["HOST"] + ":" + self.whoami["PORT"])]
                },
                chat_id=data["chat_id"],
                log_report_function=self.log_report
            )
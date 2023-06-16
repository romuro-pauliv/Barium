# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       api.services.request_data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.data_loading import DataLoadingCacheConnect
from api.connections.sender import SenderConnect
from api.connections.log import LogConnect

from api.resources.data import MESSAGES2CLIENT, WHO_AM_I

from api.utils.random_string import random_str_from_list

from typing import Any, Union
import requests
import time
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
sender_connect: SenderConnect = SenderConnect()


class RequestInitData(DataLoadingCacheConnect):
    def __init__(self) -> None:
        """
        Initialize RequestInitData instance
        """
        super().__init__()
        self.messages_keys: list[str] = ["sherlock", "request_username"]
        self.whoami: list[str] = [WHO_AM_I['NAME'], str(WHO_AM_I['HOST'] + ":" + WHO_AM_I['PORT'])]
        
    def client_responder(self, message: dict[str, Any]) -> None:
        """
        Sends the response to the client to the "Sender" service

        Args:
            message (dict[str, str]): Message from client 
        """
        chat_id: str = message["chat_id"]
        
        self.set_cache_db0_route()
        if self.post_cache({"chat_id": chat_id, "cache_value": "SHERLOCK_0"}) == True:
            for msg_key in self.messages_keys:
                
                build_json: dict[str, str] = {
                    "chat_id": chat_id,
                    "message": random_str_from_list(MESSAGES2CLIENT[msg_key]),
                    "microservice": self.whoami
                }
                
                sender_connect.send(build_json)
                time.sleep(0.5)
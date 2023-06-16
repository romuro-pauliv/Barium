# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              api.services.reply.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.sender import SenderConnect
from api.resources.data import WHO_AM_I, MESSAGES2CLIENT

from api.utils.random_string import random_str_from_list

from typing import Union
# |--------------------------------------------------------------------------------------------------------------------|


class Reply(SenderConnect):
    def __init__(self) -> None:
        """
        Initialize Reply Instance
        """
        super().__init__()
        self.whoami: list[str] = [WHO_AM_I['NAME'], str(WHO_AM_I['HOST'] + ":" + WHO_AM_I['PORT'])]
        
    def client_responder(self, message: dict[str, str]) -> None:
        """
        Sends the response to the client to the "Sender" service

        Args:
            message (dict[str, str]): Message from client 
        """
        self.msg2client: list[str] = random_str_from_list(MESSAGES2CLIENT['start'])
        
        chat_id: str = message['chat_id']
        username: str = message['username']
        
        json: dict[str, str] = {
            "chat_id": chat_id,
            "message": str(self.msg2client[0] + username + self.msg2client[1]),
            "microservice": self.whoami
        }
        
        self.send(json)
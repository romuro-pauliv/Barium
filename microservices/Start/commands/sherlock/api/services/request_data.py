# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       api.services.request_data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.data_loading import DataLoadingCacheConnect
from api.connections.sender import SenderConnect
from api.connections.data_loading import DataLoadingSherlock

from api.resources.data import MESSAGES2CLIENT, WHO_AM_I

from api.utils.random_string import random_str_from_list

from api.models.username import ModelUsername

from typing import Any, Union
import subprocess
import time
# |--------------------------------------------------------------------------------------------------------------------|

sender_connect: SenderConnect = SenderConnect()
model_username: ModelUsername  = ModelUsername()
data_loading_sherlock: DataLoadingSherlock = DataLoadingSherlock()

class RequestInitData(DataLoadingCacheConnect):
    def __init__(self) -> None:
        """
        Initialize RequestInitData instance
        """
        super().__init__()
        self.messages_keys: list[str] = ["sherlock", "request_username"]
        self.whoami: list[str] = [WHO_AM_I['NAME'], str(WHO_AM_I['HOST'] + ":" + WHO_AM_I['PORT'])]
        self.cache_ttl: int = 600 # (s)
        
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
            
            self.set_ttl_cache_db0_route()
            self.ttl_post_cache({"key": chat_id, "ttl": self.cache_ttl})


class RequestUsername(DataLoadingCacheConnect):
    def __init__(self) -> None:
        """
        Initialize RequestUsername instance
        """
        super().__init__()
        self.whoami: list[str] = [WHO_AM_I['NAME'], str(WHO_AM_I['HOST'] + ":" + WHO_AM_I['PORT'])]
        self.messages_keys: list[str] = ["init_sherlock", "finish"]
        self.cache_ttl: int = 1800 # (s)
    
    def init_sherlock(self, chat_id: str, username: str) -> None:
        """
        Starts the sherlock command
        Args:
            chat_id (str): chat_id from client
            username (str): username that the client entered in the message
        """
        command: str = f'cd Core && . venv/bin/activate && python sherlock --chatid="{chat_id}" {username} --nsfw'
        subprocess.Popen(command, shell=True)
    
    def client_responder(self, message: dict[str, Any]) -> None:
        """
        Sends the response to the client to the "Sender" service and runs Sherlock comand in sh/bash"

        Args:
            message (dict[str, Any]): Message from client
        """
        
        
        if model_username.allow_chars(message) == False:
            return None
        
        chat_id: str = message["chat_id"]
        username: str = message["text"]
        
        target_data: dict[str, Union[bool, str]] = data_loading_sherlock.get_resources_target(chat_id, username)
        if target_data != False and target_data['result'] == True:
            
            self.set_cache_db0_route()    
            self.delete_cache(chat_id)
            
            for msg_block in target_data['data']:
                build_json: dict[str, str] = {
                    "chat_id": chat_id,
                    "message": msg_block,
                    "microservice": self.whoami
                }
                sender_connect.send(build_json)
                time.sleep(0.5)
            return None
        
        self.set_cache_db0_route()
        if self.post_cache({"chat_id": chat_id, "cache_value": "SHERLOCK_STANDBY"}) == True:
            for n, msg_key in enumerate(self.messages_keys):
                
                msg: str = random_str_from_list(MESSAGES2CLIENT[msg_key])
                
                build_json: dict[str, str] = {
                    "chat_id": chat_id,
                    "message": str(msg + username) if n == 0 else msg,
                    "microservice": self.whoami
                }
                
                sender_connect.send(build_json)
                time.sleep(0.5)
            
            self.set_ttl_cache_db0_route()
            self.ttl_post_cache({"key": chat_id, "ttl": self.cache_ttl})
            
            self.init_sherlock(chat_id, username)
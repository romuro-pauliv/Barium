# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                             api.services.receiver_data_sherlock.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.data_loading import DataLoadingCacheConnect
from api.connections.sender import SenderConnect
from api.connections.log import LogConnect
from api.threads.executable import Threads

from api.resources.data import MESSAGES2CLIENT, WHO_AM_I

from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
sender_connect: SenderConnect = SenderConnect()
threads: Threads = Threads()

class ReceiverDataSherlock(DataLoadingCacheConnect):
    def __init__(self) -> None:
        """
        Initialize ReceiverDataSherlock instance
        """
        super().__init__()
        
        self.whoami: list[str] = [WHO_AM_I['NAME'], str(WHO_AM_I['HOST'] + ":" + WHO_AM_I['PORT'])]
        self.count_msg_block: dict[str, int] = {}
        self.msg_block: dict[str, int] = {}
        self.msg_block_size: int = 7
        
        self.finish_msg: str = MESSAGES2CLIENT['finish_completed'][0]
        
    def build_msg_block(self, data: dict[str, str]) -> Union[bool, dict[str, str]]:
        """
        Builds the message block with the result of the sherlock to send to the client.
        Args:
            data (dict[str, str]): Data from sherlock

        Returns:
            Union[bool, dict[str, str]]: False if the block has not yet been built. Dict with the message block and 
                                         the chat_id
        """
        chat_id: str = data["chat_id"]
        
        if data['site'] != False and data['uri'] != False:
            msg_to_build: str = "🌐 " + data["site"] + "\n" + "🔗 "+ data["uri"]
            
            # Checks the existence of the block by the chat_id
            if chat_id not in [i for i in self.count_msg_block.keys()]: 
                self.count_msg_block[chat_id] = 1
            else:
                self.count_msg_block[chat_id] += 1

            count: int = self.count_msg_block[chat_id]
            
            # If <, adds the data to the block and returns false
            if count < self.msg_block_size:
                if count != 1: # If it is not the first message, add a line break
                    self.msg_block[chat_id] += str("\n\n" + msg_to_build)
                else: # If it is the first message, it does not add a line break
                    self.msg_block[chat_id] = msg_to_build
                return False
                
            # If = add the data and return the msg block
            elif count == self.msg_block_size: 
                self.msg_block[chat_id] += str("\n\n" + msg_to_build)
            
                message: str = self.msg_block[chat_id]
            
                # Resetting chat_id variables
                del self.msg_block[chat_id]
                del self.count_msg_block[chat_id]
            
                return {"chat_id": chat_id, "message": message, "microservice": self.whoami}
        else:
            # If sherlock finished more he was still building the message block
            if chat_id in [i for i in self.count_msg_block.keys()]:
                message: str = self.msg_block[chat_id]
                
                # Resetting chat_id variables
                del self.msg_block[chat_id]
                del self.count_msg_block[chat_id]
                
                return {"chat_id": chat_id, "message": message, "microservice": self.whoami}
            else: # If the sherlock finished and there was no message block
                return {"chat_id": chat_id, "message": False, "microservice": self.whoami}
    
    def cache_signal_finish_sherlock(self, chat_id: str) -> None:
        """
        Sends a DELETE request to the DataLoading service which means that sherlock has closed processing.
        Args:
            chat_id (str): The chat_id of the client used as a key caching
        """
        self.set_cache_db0_route()
        self.delete_cache(chat_id)
    
    def sherlock_processing(self, data: dict[str, str]) -> None:
        chat_id: str = str(data['chat_id'])
        log_connect.report("REQUESTED", "SHERLOCK /BIN/SH", "info", chat_id, True)
        
        if data['site'] != False and data['uri'] != False:
            # If the sherlock has not reported the processing terminated
            
            msg_block: Union[bool, dict[str, str]] = self.build_msg_block(data)
            if msg_block != False: # If the message block is complete
                threads.start_thread(sender_connect.send, msg_block)
                
        else: # If the sherlock reported the processing terminated
            
            msg_block: Union[bool, dict[str, str]] = self.build_msg_block(data)
            
            if msg_block['message'] == False: # If there is no message block
                msg_block['message'] = self.finish_msg
                threads.start_thread(sender_connect.send, msg_block)
                self.cache_signal_finish_sherlock(chat_id)
                
            else: # If there is a message block
                msg_block['message'] += str("\n\n" + self.finish_msg)
                threads.start_thread(sender_connect.send, msg_block)
                self.cache_signal_finish_sherlock(chat_id)
                
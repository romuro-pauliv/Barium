# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.models.username.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import re
from api.connections.sender import SenderConnect
from api.connections.log import LogConnect

from api.threads.executable import Threads

from api.resources.data import WHO_AM_I, MESSAGES2CLIENT
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
sender_connect: SenderConnect = SenderConnect()
threads: Threads = Threads()

class ModelUsername(object):
    def __init__(self) -> None:
        """
        Initialize ModelUsername instance.
        """
        self.whoami: list[str] = [WHO_AM_I['NAME'], str(WHO_AM_I['HOST'] + ":" + WHO_AM_I['PORT'])]
        
        self.send_json_in_error: dict[str, str] = {
            "message": MESSAGES2CLIENT['username_error'][0],
            "microservice": self.whoami
        }
        
    def allow_chars(self, json: str) -> bool:
        """
        Validates the characters present in the username
        Args:
            username (str): Username entered by client

        Returns:
            (bool): Boolean informing the situation
        """
        chat_id: str = json["chat_id"]
        username: str = json["text"]
        
        patterns: str = r"^[A-Za-z0-9_.-]+$"
        valid_username: bool = (
            isinstance(username, str) and
            re.match(patterns, username) and
            not set(username) - set("_.-") and
            username[0] != "-"
        )
        
        if valid_username:
            return True
        else:
            log_connect.report("POST", "class<ModelUsername.allow_chars>", "error", chat_id, False, "Client Error")
            build_json: dict[str, str] = self.send_json_in_error
            build_json['chat_id'] = chat_id
            threads.start_thread(sender_connect.send(build_json))
            return False
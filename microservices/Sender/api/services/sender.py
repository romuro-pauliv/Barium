# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.services.sender.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.telegram import TelegramRequests
from api.connections.log import LogConnect
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()


class Sender(TelegramRequests):
    def __init__(self) -> None:
        """
        Initialize Sender Instance
        """
        super().__init__()
    
    def send(self, message: dict[str, str | list]) -> None:
        """
        Sends the message to the Telegram API
        Args:
            message (dict[str, str  |  list]): Message to be sent | keys -> chat_id, message, microservice
        """
        chat_id: str = message["chat_id"]
        message2client: str = message["message"]

        service_name: str = message["microservice"][0]
        service_host: str = message["microservice"][1]
        
        log_connect.report("REQUESTED", service_host, "info", chat_id, True, service_name)
        self.send_message(chat_id, message2client)
        log_connect.report("POST", self.uri_to_log, "info", chat_id, True)
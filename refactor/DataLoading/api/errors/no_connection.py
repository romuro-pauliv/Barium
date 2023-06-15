# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        api.errors.no_connection.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.log import LogConnect
from api.connections.telegram import TelegramRequests

from api.resources.data import ERROR_TELEGRAM_MESSAGE, TELEGRAM_API, LOG_REPORT
# |--------------------------------------------------------------------------------------------------------------------|

class ConnectionError(TelegramRequests):
    def __init__(self) -> None:
        """
        Initialize the ConnectionError instance.
        """
        super().__init__()
        
    def msg_2_client(self, chat_id: str) -> None:
        """
        Sends an error message to the client
        Args:
            chat_id (str): ID of the conversation with the client
        """
        self.send_message(chat_id, ERROR_TELEGRAM_MESSAGE["no_connection"])
        LogConnect().report(
            "POST", TELEGRAM_API["uri"], "info", chat_id, True,
            LOG_REPORT["connection"]["error_message_to_client"]
        )
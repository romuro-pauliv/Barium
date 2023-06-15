# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        app.errors.no_connection.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.log import LogConnect
from connections.telegram import TelegramRequests

from resources.data import ERROR_TELEGRAM_MESSAGE, TELEGRAM_API, LOG_REPORT
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()

class ConnectionError(TelegramRequests):
    def __init__(self) -> None:
        """
        Initialize the ConnectionError instance.
        """
        super().__init__()
    
    def log(self, chat_id: str) -> None:
        """
        Sends a log with log_level "info" that an error message was sent to the client
        Args:
            chat_id (str): ID of the conversation with the client
        """
        comments: str = LOG_REPORT["connection"]["error_message_to_client"]
        log_connect.report("POST", TELEGRAM_API["uri"], "info", chat_id, True, comments)
    
    def msg_2_client(self, chat_id: str) -> None:
        """
        Sends an error message to the client
        Args:
            chat_id (str): ID of the conversation with the client
        """
        self.send_message(chat_id, ERROR_TELEGRAM_MESSAGE["no_connection"])
        self.log(chat_id)
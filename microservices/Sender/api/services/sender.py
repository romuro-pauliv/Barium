# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    API.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------+
from api.config.paths import LogSchema
from api.connections.send_log import SendToLog

from api.errors.send_to_telegram import system_down_message
from api.api.api_request import TelegramApiRequest

from typing import Callable
import threading
# |--------------------------------------------------------------------------------------------------------------------|

class Sender(object):
    def __init__(self) -> None:
        self.telegram_api_request: TelegramApiRequest = TelegramApiRequest()
        self.sender: Callable[[str, str], None] = self.telegram_api_request.send_message
    
    def log_report(self, master: str, log_data: str, chat_id: str) -> None:
        """
        Send a report to LOG MS

        Args:
            master (str): Upper key in log_report.json
            log_data (str): Lower key in log_report.json
            chat_id (str): chat_id from message
        """
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
        
        threading.Thread(
            target=SendToLog().report,
            args=(log_schema[0], log_schema[1], chat_id)
        ).start()
    
    def send(self, message: dict[str, str | list]) -> None:
        threading.Thread(
            target=self.sender,
            args=(message["chat_id"], message["message"])
        ).start()
        self.log_report("connections", "sent_to_telegram", message["chat_id"])
        
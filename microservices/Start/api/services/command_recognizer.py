# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 api.services.command_recognizer.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.config.paths import MicrosservicesAPI, LogSchema

from api.connections.send_log import SendToLog
from api.connections.microservices import direct_to_ms

from typing import Any

import threading
import requests
# |--------------------------------------------------------------------------------------------------------------------|


class Driver(object):
    def __init__(self) -> None:
        """
        Loading sub microservices data routes
        """
        self.sub_services_conn: dict[str, dict] = MicrosservicesAPI.MS_ROUTES["sub_services"]
        self.commands: dict[str, str] = MicrosservicesAPI.COMMANDS
        
        self.sub_services_conn_name: list[str] = [i for i in self.commands.keys()]
    
    def log_thread(self, args_: tuple[Any]) -> None:
        """
        Execute a SendToLog().report in another thread
        Args:_
            args_ (tuple[Any]): Arguments of the function SendToLog().report
        """
        threading.Thread(target=SendToLog().report, args=args_).start()
    
    def log_report(self, HOST: str, PORT: str, log_data: str, chat_id: str) -> None:
        """
        Resume the building of the Log report
        Args:
            HOST (str): Inform the HOST executed
            PORT (str): Inform the PORT executed
            log_data (str): Lower key content log_report data
            chat_id (str): chat_id from Telegram client message
        """
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"][log_data]
        log_text: str = f"[{HOST}:{PORT}]"
        args_: tuple[str] = (log_schema[0] + log_text, log_schema[1], chat_id)
        self.log_thread(args_)
    
    def completed_connection_log(self, HOST: str, PORT: str, chat_id: str) -> None:
        self.log_report(HOST, PORT, "ms_message_response", chat_id)
    
    def failed_connection_log(self, HOST: str, PORT: str, chat_id: str) -> None:
        self.log_report(HOST, PORT, "failed_ms_message_response", chat_id)
    
    def error_message_log(self, chat_id: str) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["telegram_api"]["error_message"]
        self.log_thread((log_schema[0], log_schema[1], chat_id))
        
    def direct_to(self, message: dict[str, str | list]) -> None:
        """
        Direct the message data to specific microservice based on the given command in the message
        """
        for service_name in self.sub_services_conn_name:
            if message["text"] == self.commands[service_name]:
                direct_to_ms(
                    microservice_route_data=self.sub_services_conn,
                    command=service_name,
                    info_log=[self.completed_connection_log, self.failed_connection_log],
                    message=message,
                    error_msg_to_telegram=self.error_message_log
                )
                return None 
            
        direct_to_ms(
            microservice_route_data=self.sub_services_conn,
            command="null",
            info_log=[self.completed_connection_log, self.failed_connection_log],
            message=message,
            error_msg_to_telegram=self.error_message_log
        )
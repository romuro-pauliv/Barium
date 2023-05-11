# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 api.services.command_recognizer.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.config.paths import MicrosservicesAPI, LogSchema
from api.connections.send_log import SendToLog
from api.error.send_to_telegram import system_down_message

from typing import Callable, Any

import threading
import requests
# |--------------------------------------------------------------------------------------------------------------------|


class Driver(object):
    def __init__(self) -> None:
        self.sub_services_conn: dict[str, dict] = MicrosservicesAPI.MS_ROUTES["sub_services"]
        self.commands: dict[str, str] = MicrosservicesAPI.COMMANDS
        
        self.sub_services_conn_name: list[str] = [i for i in self.commands.keys()]
    
    def log_thread(self, func: Callable[..., None], args_: tuple[Any]) -> None:
        threading.Thread(target=func, args=args_).start()
    
    def completed_connection_log(self, HOST: str, PORT: str, chat_id: str) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["ms_message_response"]
        log_text: str = f"[{HOST}:{PORT}]"
        args_: tuple[str] = (log_schema[0] + log_text, log_schema[1], chat_id)
        self.log_thread(SendToLog().report, args_)
    
    def failed_connection_log(self, HOST: str, PORT: str, chat_id: str) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["failed_ms_message_response"]
        log_text: str = f"[{HOST}:{PORT}]"
        args_: tuple[str] = (log_schema[0] + log_text, log_schema[1], chat_id)
        self.log_thread(SendToLog().report, args_)
        
    def direct_to(self, message: dict[str, str | list]) -> None:
        for service_name in self.sub_services_conn_name:
            if message["text"] == self.commands[service_name]:
                HOST: str = self.sub_services_conn[service_name]["HOST"]
                PORT: str = self.sub_services_conn[service_name]["PORT"]
                DIR: str = self.sub_services_conn[service_name]["DIR"]
                
                try:
                    # Send to specific MS
                    print(HOST, PORT, DIR)
                    requests.post(f"{HOST}:{PORT}{DIR}", json=message)
                    self.completed_connection_log(HOST, PORT, message["chat_id"])
                    return None
                except requests.exceptions.ConnectionError:
                    system_down_message(message["chat_id"])
                    self.failed_connection_log(HOST, PORT, message["chat_id"])
                    return None
        
        # Send to null MS
        HOST: str = self.sub_services_conn["null"]["HOST"]
        PORT: str = self.sub_services_conn["null"]["PORT"]
        DIR: str = self.sub_services_conn["null"]["DIR"]
        try:    
            requests.post(f"{HOST}:{PORT}{DIR}", json=message)
            self.completed_connection_log(HOST, PORT, message["chat_id"])
        except requests.exceptions.ConnectionError:
            system_down_message(message["chat_id"])
            self.failed_connection_log(HOST, PORT, message["chat_id"])
        
        return None
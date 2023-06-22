# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               app.services.controller.post_data.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from resources.data import SERVICES_ROUTES

from connections.services import Connect
from connections.log import LogConnect

from errors.no_connection import ConnectionError

from typing import Any, Union

import requests
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
connection_error: ConnectionError = ConnectionError()

class PostController(Connect):
    def __init__(self) -> None:
        """
        Initializes an instance of the PostController.
        """
        self.route: dict[str, Any] = SERVICES_ROUTES["controller"]
        
        self.controller_route_parameter: str = self.route["controller"]["route_parameter"]
        self.controller_endpoint_home: dict[str, str] = self.route["controller"]["endpoints"]['home']
        
        super().__init__(host=self.route["HOST"], port=self.route["PORT"])
        self.set_endpoint(f"{self.controller_route_parameter}{self.controller_endpoint_home}")
    
    def log(self, success: bool, chat_id: str, comments: Union[str, None] = None) -> None:
        """
        Sends a log as a function of the "success" parameter informing about the connection status with the 
        "Controller" service
        Args:
            success (bool): If True reports a log of successful connection. If False, reports a critical error
            chat_id (str): ID of the conversation with the client
        """
        log_level: str = "info" if success == True else "error"
        log_connect.report("POST", self.uri, log_level, chat_id, success, comments)
    
    def send(self, data: dict[str, Any]) -> None:
        """
        Sends the data to the controller service
        Args:
            data (dict[str, Any]): Data received from the Telegram API and handled by the Core function
        """
        chat_id: str = data["chat_id"]
        
        response: Union[requests.models.Response, tuple[str]] = self.post(data)
        
        if not isinstance(response, requests.models.Response):
            self.log(False, chat_id, response[0])
            connection_error.msg_2_client(chat_id)
            return None
        
        self.log(True, chat_id)
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.services.driver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.services import Connect
from api.connections.log import LogConnect

from api.errors.no_connection import ConnectionError

from api.resources.data import COMMANDS, SERVICES_ROUTES

from typing import Any, Union
import requests
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
connection_error: ConnectionError = ConnectionError()


class Driver(object):
    def __init__(self) -> None:
        """
        Initialize Driver Instance
        """
        self.services_route: dict[str, Any] = SERVICES_ROUTES['services']
        self.commands_data: dict[str, Any] = COMMANDS
        self.commands_list: list[str] = [i for i in self.commands_data.keys()]
    
    def connect2service(self, route: dict[str, Union[str, dict[str, Any]]], json: dict[str, Any]) -> None:
        """
        Establishes the connection and sends the specified json file.
        Args:
            route (dict[str, Union[str, dict[str, Any]]]): Data structure informing the route (services_routes.json)
            json (dict[str, Any]): File to be sent
        """
        HOST: str = route["HOST"]
        PORT: str = route["PORT"]
        PATH: str = f"{route['receiver']['route_parameter']}{route['receiver']['endpoints']['home']}"
        
        chat_id: str = json["chat_id"]
        
        connect: Connect = Connect(HOST, PORT)
        connect.set_endpoint(PATH)
        
        response: Union[requests.models.Response, tuple[str, str]] = connect.post(json)
        
        if not isinstance(response, requests.models.Response):
            log_connect.report("POST", f"{HOST}:{PORT}{PATH}", "error", chat_id, False, response[0])
            connection_error.msg_2_client(chat_id)
            return None
        
        log_connect.report("POST", f"{HOST}:{PORT}{PATH}", "info", chat_id, True)
    
    def driver(self, json: dict[str, Any]) -> None:
        """
        Directs to the appropriate service
        Args:
            json (dict[str, Any]): File to be sent
        """
        for service_name in self.commands_list:
            if json['text'] == self.commands_data[service_name]:
                self.connect2service(self.services_route[service_name], json)
                return None
        
        self.connect2service(self.services_route['null'], json)
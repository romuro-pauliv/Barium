# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          api.connections.sender.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.services import Connect
from api.connections.log import LogConnect
from api.errors.no_connection import ConnectionError

from api.resources.data import SERVICES_ROUTES

from typing import Any, Union
import requests
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
connection_error: ConnectionError = ConnectionError()


class SenderConnect(object):
    def __init__(self) -> None:
        """
        Initialize SenderConnect Instance.
        """
        route_data: dict[str, Union[str, dict]] = SERVICES_ROUTES['sender']
        self.HOST: str = route_data['HOST']
        self.PORT: str = route_data['PORT']
        self.PATH: str = f"{route_data['receiver']['route_parameter']}{route_data['receiver']['endpoints']['home']}"
    
    def send(self, json: dict[str, Any]):
        """
        Establishes the connection and sends the specified json file
        Args:
            json (dict[str, Any]): file to be sent
        """
        connect: Connect = Connect(self.HOST, self.PORT)
        connect.set_endpoint(self.PATH)
        
        chat_id: str = json['chat_id']
        
        response: Union[requests.models.Response, tuple[str, str]] = connect.post(json)
        
        if not isinstance(response, requests.models.Response):
            log_connect.report("POST", f"{self.HOST}:{self.PORT}{self.PATH}", "error", chat_id, False, response[0])
            connection_error.msg_2_client(chat_id)
            return None

        log_connect.report("POST", f"{self.HOST}:{self.PORT}{self.PATH}", "info", chat_id, True)
        
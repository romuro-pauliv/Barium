# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    api.connections.data_loading.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.services import Connect
from connections.log import LogConnect

from resources.data import SERVICES_ROUTES

from typing import Union, Any
import requests
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()


class ClientDataConnect(Connect):
    def __init__(self) -> None:
        """
        Initialize ClientDataConnect instance and connect to data loading route
        """
        route_data: dict[str, Any] = SERVICES_ROUTES['data_loading']
        HOST: str = route_data['HOST']
        PORT: str = route_data['PORT']
        ROUTE_PARAMETER: str = route_data['client-data']['route_parameter']
        ENDPOINT: str = route_data['client-data']['endpoints']['home']
        
        super().__init__(HOST, PORT)
        self.set_endpoint(f"{ROUTE_PARAMETER}{ENDPOINT}")
        
        self.uri_to_log: str = f"{HOST}:{PORT}{ROUTE_PARAMETER}{ENDPOINT}"
        
    def get_chat_ids(self) -> list[int]:
        """
        Makes a GET request to /client-data in the data_loading service and returns a list with the ids of the clients
        already active in the database.
        
        Returns:
            list[int]: list object with the chat_id of the clients
        """
        response: Union[requests.models.Response, tuple[str, str]] = self.get()
        if not isinstance(response, requests.models.Response):
            log_connect.report("GET", self.uri_to_log, 'error', "INTERNAL", False)
            return []
        
        log_connect.report("GET", self.uri_to_log, "info", "INTERNAL", True)
        return response.json()
    
    def post_client_data(self, data: dict[str, Any]) -> None:
        """
        For a new client connects to the system, it sends the data to the data_loading service with the client's data
        Args:
            data (dict[str, Any]): dict with the client's data
        """
        response: Union[requests.models.Response, tuple[str, str]] = self.post(data)
        if not isinstance(response, requests.models.Response):
            log_connect.report("POST", self.uri_to_log, 'error', "INTERNAL", False)
            return None
        
        log_connect.report("POST", self.uri_to_log, "info", "INTERNAL", True)
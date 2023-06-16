# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    api.connections.data_loading.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.connections.services import Connect
from api.connections.log import LogConnect

from api.errors.no_connection import ConnectionError

from api.resources.data import SERVICES_ROUTES

from typing import Union, Any
import requests
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()
connection_error: ConnectionError = ConnectionError()

class DataLoadingCacheConnect(object):
    def __init__(self) -> None:
        """
        Initialize DataLoadingCacheConnect Instance and initialize the connection with data_loading service
        """
        self.route_data: dict[str, Any] = SERVICES_ROUTES['data_loading']
        self.HOST: str = self.route_data["HOST"]
        self.PORT: str = self.route_data["PORT"]

        self.connect: Connect = Connect(self.HOST, self.PORT)
        
    def set_cache_db0_route(self) -> None:
        """
        Sets the route to /cache/db0
        """
        self.route_parameter: str = self.route_data['cachedb0']['route_parameter']
        self.endpoint: str = self.route_data['cachedb0']['endpoints']['home']    
        self.connect.set_endpoint(f"{self.route_parameter}{self.endpoint}")
    
    def post_cache(self, json: dict[str, Any]) -> bool:
        """
        It makes a POST request to the "Data Loading" service. You must use some method to define the route before
        Args:
            json (dict[str, Any]): Json containing the caching. | keys -> chat_id, cache_value
        """
        uri_to_log: str = f"{self.HOST}:{self.PORT}{self.route_parameter}{self.endpoint}"
        
        chat_id: str = json["chat_id"]
        
        response: Union[requests.models.Response, tuple[str, str]] = self.connect.post(json)
        
        if not isinstance(response, requests.models.Response):
            log_connect.report("POST", uri_to_log, "error", chat_id, False, response[0])
            connection_error.msg_2_client(chat_id)
            return False
        
        log_connect.report("POST", uri_to_log, "info", chat_id, True)
        return True
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
    
    def set_ttl_cache_db0_route(self) -> None:
        """
        Sets the route to /cache/ttl-db0
        """
        self.route_parameter: str = self.route_data['cachedb0']['route_parameter']
        self.endpoint: str = self.route_data['cachedb0']['endpoints']['ttl']    
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
    
    def delete_cache(self, key: str) -> bool:
        """
        It makes a DELETE request to the "Data Loading" service. You must use some method to define the route before
        Args:
            key (dict[str, Any]): Key data to delete
        """
        uri_to_log: str = f"{self.HOST}:{self.PORT}{self.route_parameter}{self.endpoint}"
        
        chat_id: str = key
        json: dict[str, str] = {"chat_id": key}
        
        response: Union[requests.models.Response, tuple[str, str]] = self.connect.delete(json)
        
        if not isinstance(response, requests.models.Response):
            log_connect.report("DELETE", uri_to_log, "error", chat_id, False, response[0])
            connection_error.msg_2_client(chat_id)
            return False
        
        log_connect.report("DELETE", uri_to_log, "info", chat_id, True)
        return True
    
    def ttl_post_cache(self, json: dict[str, Any]) -> bool:
        """
        It makes a POST request to the "Data Loading" service. You must use some method to define the route before
        Args:
            json (dict[str, Any]): Json containing the ttl caching. | keys -> key, ttl
        """
        uri_to_log: str = f"{self.HOST}:{self.PORT}{self.route_parameter}{self.endpoint}"
        
        chat_id: str = json["key"]
        
        response: Union[requests.models.Response, tuple[str, str]] = self.connect.post(json)
        
        if not isinstance(response, requests.models.Response):
            log_connect.report("POST", uri_to_log, "error", chat_id, False, response[0])
            connection_error.msg_2_client(chat_id)
            return False
        
        log_connect.report("POST", uri_to_log, "info", chat_id, True, "TTL")
        return True

class DataLoadingSherlock(object):
    def __init__(self) -> None:
        self.route_data: dict[str, Any] = SERVICES_ROUTES['data_loading']
        self.HOST: str = self.route_data["HOST"]
        self.PORT: str = self.route_data["PORT"]
        
        self.connect: Connect = Connect(self.HOST, self.PORT)
    
    def post_resources_target(self, chat_id: str, target_username: str, sherlock_data: str) -> None:
        route_parameter: str = self.route_data['sherlock']['route_parameter']
        endpoint: str = self.route_data['sherlock']['endpoints']['post-target']
        self.connect.set_endpoint(f"{route_parameter}{endpoint}")
        
        uri_to_log: str = f"{self.HOST}:{self.PORT}{route_parameter}{endpoint}"
        
        build_json: dict[str, Union[str, dict[str, Any]]] = {
            "chat_id": chat_id,
            "target_username": target_username,
            "sherlock_data": sherlock_data
        }
        
        response: Union[requests.models.Response, tuple[str, int]] = self.connect.post(build_json)
        
        if not isinstance(response, requests.models.Response):
            log_connect.report("POST", uri_to_log, "error", chat_id, False, "non-saved target data")
            return False
        
        log_connect.report("POST", uri_to_log, "info", chat_id, True, "target data saved")
        return True
    
    def get_resources_target(self, chat_id: str, target: str) -> tuple[dict[str, Union[str, bool]]]:
        """
        Establishes connection with the DataLoading service and requests the target data
        Args:
            chat_id (str): Client's chat_id
            target (str): Target informed by the client

        Returns:
            tuple[dict[str, Union[str, bool]]]: User data with search status
        """
        route_parameter: str = self.route_data['sherlock']['route_parameter']
        endpoint: str = self.route_data['sherlock']['endpoints']['get-target']
        self.connect.set_endpoint(f"{route_parameter}{endpoint}")
        
        uri_to_log: str = f"{self.HOST}:{self.PORT}{route_parameter}{endpoint}"
        
        build_json: dict[str, str] = {
            "chat_id": chat_id,
            "target": target
        }
        
        response: Union[requests.models.Response, tuple[str, str]] = self.connect.get(build_json)

        if not isinstance(response, requests.models.Response):
            log_connect.report("GET", uri_to_log, "error", chat_id, False)
            return False
        
        log_connect.report("GET", uri_to_log, "info", chat_id, True)
        return response.json()
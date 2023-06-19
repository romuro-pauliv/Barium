# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           api.controller.driver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.errors.no_connection import ConnectionError

from api.connections.cache import CacheConnect, CacheDB
from api.connections.log import LogConnect
from api.connections.data_loading import Session
from api.connections.services import Connect

from api.resources.data import SERVICES_ROUTES

from typing import Union
import requests
# |--------------------------------------------------------------------------------------------------------------------|

class Data(object):
    """
    Stores route data in instance for ease of use
    """
    class StartService(object):
        """
        Start Service Route Data
        """
        @staticmethod
        def host() -> str:
            return SERVICES_ROUTES['start_service']['HOST']
        
        @staticmethod
        def port() -> str:
            return SERVICES_ROUTES['start_service']['PORT']
        
        @staticmethod
        def endpoint() -> str:
            route_parameter: str = SERVICES_ROUTES['start_service']['receiver']['route_parameter']
            endpoint: str = SERVICES_ROUTES['start_service']['receiver']['endpoints']['home']
            return f"{route_parameter}{endpoint}"

    class SherlockService(object):
        """
        Sherlock Service Route Data
        """
        @staticmethod
        def host() -> str:
            return SERVICES_ROUTES['sherlock_service']['HOST']
        
        @staticmethod
        def port() -> str:
            return SERVICES_ROUTES['sherlock_service']['PORT']
        
        @staticmethod
        def endpoint_receiver() -> str:
            route_parameter: str = SERVICES_ROUTES['sherlock_service']['receiver']['route_parameter']
            endpoint: str = SERVICES_ROUTES['sherlock_service']['receiver']['endpoints']['home']
            return f"{route_parameter}{endpoint}"

        @staticmethod
        def endpoint_username() -> str:
            route_parameter: str = SERVICES_ROUTES['sherlock_service']['username']['route_parameter']
            endpoint: str = SERVICES_ROUTES['sherlock_service']['username']['endpoints']['home']
            return f"{route_parameter}{endpoint}"

class Driver(object):
    def __init__(self) -> None:
        """
        Initialize Driver instances
        """
        session: Session = Session()
        self.session: list[str] = session.get()
        self.log_connect: LogConnect = LogConnect()
        
    def post_data_in(self, host: str, port: str, endpoint: str, json: dict[str, str]) -> None:
        """
        It establishes a connection to the service you entered and sends the data. Already provides log support
        Args:
            host (str): service host
            port (str): service port
            endpoint (str): service endpoint
            json (dict[str, str]): Date that will be sent to the service
        """
        connect: Connect = Connect(host, port)
        connect.set_endpoint(endpoint)
        
        chat_id: str = json["chat_id"]
        full_uri: str = f"{host}:{port}{endpoint}"
        
        response: Union[requests.models.Response, tuple[str, str]] = connect.post(json)
        
        if not isinstance(response, requests.models.Response):
            self.log_connect.report("POST", full_uri, "error", chat_id, False, response[0])
            ConnectionError().msg_2_client(chat_id)
            return None
        
        self.log_connect.report("POST", full_uri, "info", chat_id, True)
        
    def drive(self, message: dict[str, str | list]) -> None:
        """
        Directs or service indicated depending on the data present in the message
        Args:
            message (dict[str, str  |  list]): Data received from the Gateway
        """
        chat_id: str = message['chat_id']
        
        if not isinstance(self.session, list):
            ConnectionError().msg_2_client(chat_id)
            return None

        if chat_id not in self.session:
            cache: Union[bool, str] = CacheConnect(CacheDB.db0).get(chat_id)
            if cache != False:
                message["cache"] = cache
                
                if cache == "SHERLOCK_0":
                    self.post_data_in(
                        Data.SherlockService.host(), Data.SherlockService.port(),
                        Data.SherlockService.endpoint_username(), message
                    )
                    return None

            self.post_data_in(Data.StartService.host(), Data.StartService.port(), Data.StartService.endpoint(), message)
                
        
        
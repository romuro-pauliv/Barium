# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    api.connections.data_loading.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.threads.executable import Threads

from api.resources.data import SERVICES_ROUTES

from api.connections.services import Connect
from api.connections.log import LogConnect

import requests
from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|

data_loading_rt: dict[str, Any] = SERVICES_ROUTES['data_loading']
log_connect: LogConnect = LogConnect()
threads: Threads = Threads()


class Session(object):
    def __init__(self) -> None:
        """
        Initialize Session Connection instance
        """
        host: str = data_loading_rt['HOST']
        port: str = data_loading_rt['PORT']
        route_parameter: str = data_loading_rt['session']['route_parameter']
        endpoint: str = data_loading_rt['session']['endpoints']['home']
        
        self.connect: Connect = Connect(host, port)
        self.connect.set_endpoint(f"{route_parameter}{endpoint}")
        self.full_uri: str = f"{host}:{port}{route_parameter}{endpoint}"
        
    def get(self) -> Union[list[str], bool]:
        """
        Makes a GET request on the data_loading service and returns the user sessions
        Returns:
            Union[list[str], bool]: Returns the user session or False if it failed to establish the session request
        """
        response: Union[requests.models.Response, tuple[str, str]] = self.connect.get()
        
        if not isinstance(response, requests.models.Response):
            threads.start_thread(log_connect.report, "GET", self.full_uri, "error", 'INTERNAL', False, response[0])
            return False
        
        threads.start_thread(log_connect.report, "GET", self.full_uri, "info", 'INTERNAL', True)
        return response.json()
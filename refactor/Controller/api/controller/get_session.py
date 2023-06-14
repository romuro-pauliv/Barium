# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      api.controller.get_session.py |
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

log_connect: LogConnect = LogConnect()
threads: Threads = Threads()

# | Data Loading Connect |---------------------------------------------------------------------------------------------|
data_loading_rt: dict[str, Any] = SERVICES_ROUTES['data_loading']
CONNECT_DATA_LOADING: Connect = Connect(data_loading_rt['HOST'], data_loading_rt['PORT'])
# | -------------------------------------------------------------------------------------------------------------------|

# | Set endpoint to /session/ |----------------------------------------------------------------------------------------|
session_route_parameter: str =  data_loading_rt['session']['route_parameter']
session_endpoint: str = data_loading_rt['session']['endpoints']['home']
CONNECT_DATA_LOADING.set_endpoint(f"{session_route_parameter}{session_endpoint}")
# |--------------------------------------------------------------------------------------------------------------------|

uri_to_log: str = f"{data_loading_rt['HOST']}:{data_loading_rt['PORT']}{session_route_parameter}{session_endpoint}"

class Session(object):
    def get(self) -> Union[list[str], bool]:
        """
        Makes a GET request on the data_loading service and returns the user sessions
        Returns:
            Union[list[str], bool]: Returns the user session or False if it failed to establish the session request
        """
        response: Union[requests.models.Response, tuple[str, str]] = CONNECT_DATA_LOADING.get()
        
        if not isinstance(response, requests.models.Response):
            threads.start_thread(log_connect.report, "GET", uri_to_log, "error", 'INTERNAL', False, response[0])
            return False
        
        threads.start_thread(log_connect.report, "GET", uri_to_log, "info", 'INTERNAL', True)
        return response.json()
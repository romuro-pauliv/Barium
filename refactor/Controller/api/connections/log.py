# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             app.connections.log.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from connections.services import Connect

from log.local_log import LocalLog

from resources.data import SERVICES_ROUTES, WHO_AM_I

from typing import Union, Any

import requests
# |--------------------------------------------------------------------------------------------------------------------|

class BuildLogJson(object):
    def build_json(self, chat_id: str) -> dict[str, Union[str, dict]]:
        """
        Builds a base json with its own process information and the customer's chat_id
        Args:
            chat_id (str): ID of the conversation with the client
        Returns:
            dict[str, Union[str, dict]]: Incomplete JSON payload for the [auto] or [commented] build_json
        """
        return {
            "extra": {
                "microservice": WHO_AM_I['NAME'],
                "clientip": str(WHO_AM_I['HOST'] + WHO_AM_I['PORT']),
                "chat_id": chat_id
            }
        }

    def log_json(
        self, http_method: str, service_route: str,
        chat_id: str, success: bool, comments: Union[str, None] = None) -> dict[str, Union[str, dict]]:
        """
        Build the JSON payload for the log report.
        Args:
            http_method (str): HTTP method used for communication with the specified service
            service_route (str): Service that the communication was made
            chat_id (str): ID of the conversation with the client
            success (bool): Whether it was successful or not
        Returns:
            dict[str, Union[str, dict]]: JSON payload for the log report.
        """
        json_data: dict[str, Union[str, dict]] = self.build_json(chat_id)
        
        success_string: str = "Success" if success == True else "Failed"
        json_data["report"] = f"{success_string} on {http_method.upper()} in {service_route.lower()}"
        if comments != None:
            json_data["report"] += f" - {comments}"
        return json_data


class LogConnect(Connect, BuildLogJson, LocalLog):
    def __init__(self) -> None:
        """
        Initialize the LogConnect instance.
        """
        self.log_route: dict[str, Any] = SERVICES_ROUTES["log"]
        
        self.report_log_parameter: str = self.log_route["report_log"]["route_parameter"]
        self.report_log_endpoints: dict[str, str] = self.log_route["report_log"]["endpoints"]
        
        super().__init__(host=self.log_route["HOST"], port=self.log_route["PORT"])
    
    def report(
        self, http_method: str, service_route: str,
        log_level: str, chat_id: str, success: bool, comments: Union[str, None] = None) -> None:
        """
        Post a report to the log service.
        Args:
            http_method (str): HTTP method used for communication with the specified service
            service_route (str): Service that the communication was made
            log_level (str): Log level ["debug", "info", "warning", "error", "critical"].
            chat_id (str): ID of the conversation with the client
            success (bool): Whether it was successful or not
        """
        self.set_endpoint(f"{self.report_log_parameter}{self.report_log_endpoints[log_level]}")
        
        json: dict[str, str] = self.log_json(http_method, service_route, chat_id, success, comments)
        response: Union[requests.models.Response, tuple[str, str]] = self.post(json)
        
        if not isinstance(response, requests.models.Response):
            self.save(json)
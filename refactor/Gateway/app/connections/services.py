# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        api.connections.services.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from typing import Union, Any
# |--------------------------------------------------------------------------------------------------------------------|


class Connect(object):
    def __init__(self, host: str, port: str) -> None:
        """
        Initializes an instance of the Connect class.
        Args:
            host (str): The host address of the API.
            port (str): The port of the API.
        Returns:
            None
        """
        self.host: str = host
        self.port: str = port
        self.endpoint: str = "/"
        self.uri: str = f"{self.host}:{self.port}{self.endpoint}"
    
    def __repr__(self) -> str:
        return f"Connect(host='http://example.com', port='5000')"
        
    def set_endpoint(self, path_: str) -> None:
        """
        Sets the endpoint of the API.
        Args:
            path_ (str): The path of the API endpoint.
        Returns:
            None
        """
        self.endpoint: str = path_
        self.uri: str = f"{self.host}:{self.port}{self.endpoint}"
    
    def make_request(self, method: str,
                     json: Union[dict[str, Any], None] = None) -> Union[requests.models.Response, tuple[str, str]]:
        """
        Makes a generic HTTP request.
        Args:
            method (str): The HTTP method of the request (GET, POST, PUT, DELETE).
            json (Union[dict[str, Any], None], optional): The JSON data to be sent in the request. Defaults to None.
        Returns:
            Union[requests.models.Response, tuple[str, str]]: The response of the request or a tuple representing the
                                                              occurred error.
        """
        try:
            response: requests.models.Response = requests.request(method, self.uri, json=json)
            return response
        except requests.exceptions.HTTPError as errh:
            return "HTTP Error", errh
        except requests.exceptions.ProxyError as errp:
            return "Proxy Error", errp
        except requests.exceptions.ConnectionError as errc:
            return "Error Connecting", errc
        except requests.exceptions.Timeout as errt:
            return "Timeout Error", errt
        except requests.exceptions.RequestException as err:
            return "Unknown Error", err

    def get(self, json: Union[dict[str, Any], None] = None) -> Union[requests.models.Response, tuple[str, str]]:
        """
        Makes an HTTP GET request.
        Args:
            json (Union[dict[str, Any], None], optional): The JSON data to be sent in the request. Defaults to None.
        Returns:
            Union[requests.models.Response, tuple[str, str]]: The response of the request or a tuple representing the
                                                              occurred error.
        """
        return self.make_request("GET", json)
    
    def post(self, json: Union[dict[str, Any], None] = None) -> Union[requests.models.Response, tuple[str, str]]:
        """
        Makes an HTTP POST request.
        Args:
            json (Union[dict[str, Any], None], optional): The JSON data to be sent in the request. Defaults to None.
        Returns:
            Union[requests.models.Response, tuple[str, str]]: The response of the request or a tuple representing the
                                                              occurred error.
        """
        return self.make_request("POST", json)
    
    def put(self, json: Union[dict[str, Any], None] = None) -> Union[requests.models.Response, tuple[str, str]]:
        """
        Makes an HTTP PUT request.
        Args:
            json (Union[dict[str, Any], None], optional): The JSON data to be sent in the request. Defaults to None.
        Returns:
            Union[requests.models.Response, tuple[str, str]]: The response of the request or a tuple representing the
                                                              occurred error.
        """
        return self.make_request("PUT", json)

    def delete(self, json: Union[dict[str, Any], None] = None) -> Union[requests.models.Response, tuple[str, str]]:
        """
        Makes an HTTP POST request.
        Args:
            json (Union[dict[str, Any], None], optional): The JSON data to be sent in the request. Defaults to None.
        Returns:
            Union[requests.models.Response, tuple[str, str]]: The response of the request or a tuple representing the
                                                              occurred error.
        """
        return self.make_request("DELETE", json)

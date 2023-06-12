# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        api.connections.services.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
import threading
from typing import Union, Any
# |--------------------------------------------------------------------------------------------------------------------|


class Connect(object):
    def __init__(self, host: str, port: str) -> None:
        self.host: str = host
        self.port: str = port
        self.endpoint: str = "/"
    
    def endpoint(self, path: str) -> None:
        self.endpoint: str = path
    
    def get(self, json: Union[dict[str, Any], None] = None, in_thread: bool = True) -> tuple[Any, int]:
        if in_thread == True:
            return threading.Thread(
                target=requests.post,
                kwargs={'url':f"{self.host}:{self.port}{self.endpoint}", 'json': json}
            ).start()
        else:
            response: tuple[Any, int] = requests.get(f"{self.host}:{self.port}{self.endpoint}", json=json)
            return response


controller: Connect = Connect("http://127.0.0.1", "5000")
controller.endpoint(path="/controller/")

print(controller.get(None, False))

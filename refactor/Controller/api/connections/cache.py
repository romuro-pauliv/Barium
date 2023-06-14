# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           api.connections.cache.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Union

from api.connections.log import LogConnect

from redis import Redis, client
from dotenv import load_dotenv
import os
# |--------------------------------------------------------------------------------------------------------------------|

log_connect: LogConnect = LogConnect()

load_dotenv()
HOST: str = os.getenv("REDIS_HOST")
PORT: str = os.getenv("REDIS_PORT")

class CacheDB(object):
    """
    _Caching instance
    """
    db0: client.Redis = Redis(HOST, PORT, db=0)


class CacheConnect(object):
    def __init__(self, connect_instance: client.Redis) -> None:
        """
        Initialize CacheConnect instance
        Args:
            connect_instance (client.Redis): Connection object from CacheDB instance
        """
        self.cachedb: client.Redis = connect_instance
        self.uri_to_log: str = f"{HOST}:{PORT}:db{self.cachedb.client_info()['db']}"

    def get(self, key: str) -> Union[bool, str]:
        """
        Verify and GET Redis cache data
        Args:
            key (str): Key in Redis Cache

        Returns:
            Union[bool, str]: False if not cache or str if cache exists
        """
        response: Union[None, str] = self.cachedb.get(key)
        if response == None:
            log_connect.report("GET", self.uri_to_log, "info", 'INTERNAL', True, 'Cache-Free')
            return False
        else:
            log_connect.report("GET", self.uri_to_log, "info", 'INTERNAL', True)
            return response.decode('utf-8')
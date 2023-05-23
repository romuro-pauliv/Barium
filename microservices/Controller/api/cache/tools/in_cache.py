# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        api.cache.tools.in_cache.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from redis import client
from typing import Union
import threading

from api.connections.send_log import SendToLog
from api.config.paths import LogSchema
# |--------------------------------------------------------------------------------------------------------------------|

def get_cache_log_report(key: str) -> None:
    """
    Report to LOG MS that was estabilished a connection with REDIS
    Args:
        key (str): Key sought
    """
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["get_cache_in_redis"]
    
    threading.Thread(
        target=SendToLog().report,
        args=(log_schema[0], log_schema[1], key)
    ).start()


def get_cache(instance: client.Redis, key: str) -> Union[bool, str]:
    """
    Verify and return Redis cache data
    Args:
        instance (client.Redis): instance from Redis connect
        key (str): Key in Redis Cache

    Returns:
        Union[bool, str]: False if not cache or str if cache exists
    """
    get_cache_log_report(key)
    cache: Union[None, str] = instance.get(key)
    return False if cache == None else cache.decode('utf-8')
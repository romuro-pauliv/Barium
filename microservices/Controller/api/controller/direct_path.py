# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      api.controller.direct_path.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Union

from api.cache.redis_connect import Cache
from api.cache.tools.in_cache import get_cache

from api.controller.get_session import Session

from api.errors.send_to_telegram import system_down_message

from api.connections.send_log import SendToLog
from api.config.paths import LogSchema, MicrosservicesAPI
import requests
# |--------------------------------------------------------------------------------------------------------------------|

# Session Request 
session: Session = Session()
session_trigger: bool = session.request()
session_list: list[str] = session.get()

# Connection to start | client Driver
ms_start: dict[str, dict[str, str]] = MicrosservicesAPI.MS_ROUTES["ms_start"]

# Log Report
def log_report(master: str, log_data: str, message: str) -> None:
    """
    Resume a connection with SendToLog class to send a log report to Log MS
    Args:
        master (str): Higher key in log_report.json
        log_data (str): Lower key in log_report.json
        message (str): Message content chat_id
    """
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
    SendToLog().report(log_schema[0], log_schema[1], message["chat_id"])

def post_in_microservice(route: dict[str, str], log_data: list[str, str], message: dict[str]) -> None:
    """
    Send the message to specific microservice.
    Args:
        route (dict[str, str]): Route in ms_routes.json
        log_data (list[str, str]): In [0] sucessfully key in log_report.json and [1] failed key in log_report.json
        message (dict[str]): Message from Gateway
    """
    try:
        requests.post(f"{route['HOST']}:{route['PORT']}{route['PATH1']}{route['ENDPOINTS']['home']}", json=message)
        log_report("connections", log_data[0], message)
    except requests.exceptions.ConnectionError:
        log_report("connection", log_data[1], message)
        system_down_message(message["chat_id"])
        log_report("telegram_api", "error_message", message)
        
# | DRIVER |===========================================================================================================|
def driver(message: dict[str, str | list]) -> None:
    """
    Driver the message data (handled or not) to specific microservice.
    Args:
        message (dict[str, str  |  list]): Message data from Gateway
    """
    if session_trigger == False:
        system_down_message(message["chat_id"])
        log_report("telegram_api", "error_message", message)
        return None
    
    if message["chat_id"] not in session_list:
        cache: Union[bool, str] = get_cache(Cache.TalkCache.db0_cache, message["chat_id"])
        if cache != False:
            message["cache"] = cache
        post_in_microservice(ms_start, ["start_driver_completed", "start_driver_failed"], message)
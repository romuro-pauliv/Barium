# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      api.controller.direct_path.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.cache.redis_connect import Cache
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

# Log Schema in error message
log_schema_user_error: list[str] = LogSchema.LOG_REPORT_MSG["telegram_api"]["error_message"]
log_schema_connections: dict[str, list[str]] = LogSchema.LOG_REPORT_MSG["connections"]

# Connection to start | client Driver
ms_start: dict[str, dict[str, str]] = MicrosservicesAPI.MS_ROUTES["ms_start"]

def driver(message: dict[str, str | list]) -> None:
    if session_trigger == False:
        system_down_message(message["chat_id"])
        SendToLog().report(log_schema_user_error[0], log_schema_user_error[1], message["chat_id"])
        return None
    
    try:
        requests.post(f"{ms_start['HOST']}:{ms_start['PORT']}{ms_start['DIR']}", json=message)
        # Send to Log MS
        log_completed: list[str] = log_schema_connections["start_driver_completed"]
        SendToLog().report(log_completed[0], log_completed[1], message["chat_id"])
    
    except requests.exceptions.ConnectionError:
        # Send to Log MS
        log_failed: list[str] = log_schema_connections["start_driver_failed"]
        SendToLog().report(log_failed[0], log_failed[1], message["chat_id"])
        
        system_down_message(message["chat_id"])
        # Send to Log MS
        SendToLog().report(log_schema_user_error[0], log_schema_user_error[1], message["chat_id"])
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
from api.config.paths import LogSchema
# |--------------------------------------------------------------------------------------------------------------------|

# Session Request 
session: Session = Session()
session_trigger: bool = session.request()
session_list: list[str] = session.get()

# Log Schema in error message
log_schema: list[str] = LogSchema.LOG_REPORT_MSG["telegram_api"]["error_message"]

def driver(message: str) -> None:
    if session_trigger == False:
        system_down_message(message["chat_id"])
        SendToLog().report(log_schema[0], log_schema[1], message["chat_id"])
        return None
    
    if message["chat_id"] in session_list:
        print("In Session")
    else:
        print("No Session")
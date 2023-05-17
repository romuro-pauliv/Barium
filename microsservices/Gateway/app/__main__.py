# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from core.last_message import Core
from connections.send_controller import SendToController

from connections.send_log import SendToLog
from config.paths import LogSchema

import threading
# |--------------------------------------------------------------------------------------------------------------------|

core = Core()

while True:
    last_message: dict[str, dict[str, str]] = core.last_message()
    if last_message:
        for id_ in last_message.keys():
            data = last_message[id_]
            data["chat_id"] = str(id_)
            
            # POST in log API |----------------------------------------------------------------------------------------|
            log_schema: list[str] = LogSchema.LOG_REPORT_MSG["telegram_api"]["received_update"]
            threading.Thread(target=SendToLog().report, args=(log_schema[0], log_schema[1], str(id_),)).start()
            # |--------------------------------------------------------------------------------------------------------|
            
            # POST in controller API |---------------------------------------------------------------------------------|
            threading.Thread(target=SendToController().post, args=(data,)).start()
            # |--------------------------------------------------------------------------------------------------------|
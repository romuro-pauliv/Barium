# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.services.command_recognizer import Driver
import threading

from api.config.paths import LogSchema
from api.connections.send_log import SendToLog
# |--------------------------------------------------------------------------------------------------------------------|

# Blueprint
bp = Blueprint("start", __name__)

# Driver Loading
driver: Driver = Driver()

# log
def log_report(chat_id: str) -> None:
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_message_from_controller"]
    threading.Thread(
        target=SendToLog().report,
        args=(log_schema[0], log_schema[1], chat_id)
    ).start()

@bp.route("/", methods=["POST"])
def message_receiver() -> tuple[str, int]:    
    log_report(request.json["chat_id"])
    threading.Thread(target=driver.direct_to, args=(request.json,)).start()
    return "OK", 202
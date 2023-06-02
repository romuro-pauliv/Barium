# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import threading
from flask import Blueprint, request
from api.config.paths import LogSchema
from api.connections.send_log import SendToLog
# |--------------------------------------------------------------------------------------------------------------------|

bp_inform_username: Blueprint = Blueprint("in-cache", __name__)

def log_report(chat_id: str) -> None:
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_message_controller"]
    threading.Thread(
        target=SendToLog().report,
        args=(log_schema[0], log_schema[1], chat_id)
    ).start()

@bp_inform_username.route("/", methods=["POST"])
def receiver() -> tuple[str, int]:
    print("OK")
    return "OK", 202
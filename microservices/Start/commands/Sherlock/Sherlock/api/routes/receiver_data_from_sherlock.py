# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                          API.routes.receiver_data_from_sherlock.py |
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

bp_receiver_data_from_sherlock: Blueprint = Blueprint("receiver_data", __name__)

def log_report(chat_id: str) -> None:
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_data_sherlock"]
    threading.Thread(
        target=SendToLog().report,
        args=(log_schema[0], log_schema[1], chat_id)
    ).start()

@bp_receiver_data_from_sherlock.route("/", methods=["POST"])
def receiver() -> tuple[str, int]:
    print(request.json)
    return "OK", 202
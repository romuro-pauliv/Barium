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

from api.services.received_data_from_sherlock import ReceivedDataSherlock
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
    
    log_report(request.json["chat_id"])
    
    threading.Thread(
        target=ReceivedDataSherlock().send,
        args=(request.json, )
    ).start()
    
    return "OK", 202
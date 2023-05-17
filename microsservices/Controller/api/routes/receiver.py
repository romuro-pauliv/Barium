# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.controller.direct_path import driver
from api.connections.send_log import SendToLog
from api.config.paths import LogSchema
import threading
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("controller", __name__)

def log_report(master: str, log_data: str, chat_id: str) -> None:
    """
    Resume a connection with SendToLog class to send a log report to Log MS
    Args:
        master (str): Higher key in log_report.json
        log_data (str): Lower key in log_report.json
        chat_id (str): chat_id from message data
    """
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG[master][log_data]
    threading.Thread(
        target=SendToLog().report, args=(
            log_schema[0], log_schema[1], chat_id
        )
    ).start()


@bp.route("/", methods=["POST"])
def message_receiver() -> tuple[str, int]:    
    log_report("connections", "received_message_data_gateway", request.json["chat_id"])
    threading.Thread(target=driver, args=(request.json, )).start()    
    return "OK", 202
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

# Log schema
log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_message_data_gateway"]

@bp.route("/", methods=["POST"])
def message_receiver() -> tuple[str, int]:    
    
    threading.Thread(target=driver, args=(request.json, )).start()
    # Send to Log MS
    threading.Thread(
        target=SendToLog().report, args=(
            log_schema[0], log_schema[1], request.json["chat_id"],
        )
    ).start()
    
    return "OK", 202
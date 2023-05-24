# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    API.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import threading
from flask import Blueprint, request
from api.config.paths import LogSchema
from api.connections.send_log import SendToLog

from api.services.respond_client import RespondClient
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("help", __name__)

def log_report(chat_id: str) -> None:
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_from_start_driver"]
    threading.Thread(
        target=SendToLog().report,
        args=(log_schema[0], log_schema[1], chat_id)
    ).start()
        
respond_client: RespondClient = RespondClient()

@bp.route("/", methods=["POST"])
def receiver() -> tuple[str, int]:
    log_report(request.json["chat_id"])
            
    threading.Thread(
        target=respond_client.post,
        args=(request.json,)
    ).start()
            
    return "OK", 202
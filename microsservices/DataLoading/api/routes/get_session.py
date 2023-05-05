# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          api.routes.get_session.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint
from api.services.session.handling_session import Session

import threading

from api.config.paths import LogSchema
from api.connections.send_log import SendToLog
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("session", __name__)

# Service Class
session = Session()

# Log Schema
log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["get_controller"]

@bp.route("/", methods=["GET"])
def get_session() -> tuple[list[str], int]:
    # Send to LOG MS
    threading.Thread(target=SendToLog().report, args=(log_schema[0], log_schema[1], log_schema[2])).start()
    
    # Response request with sessions list
    return session.get(), 200
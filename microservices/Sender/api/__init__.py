# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    API.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------+
import threading

from flask import Flask, request
from typing import Union

from .services.sender import Sender
from .config.paths import LogSchema
from .connections.send_log import SendToLog
# |--------------------------------------------------------------------------------------------------------------------+


def create_app(test_config: Union[bool, None] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping()
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # Route
    sender: Sender = Sender()
    def log_report(ms_name: str, ms_host: str, chat_id: str) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_from_command"]
        threading.Thread(
            target=SendToLog().report,
            args=(str(log_schema[0] + ms_name + " " + "[" + ms_host + "]"), log_schema[1], chat_id)
        ).start()
    
    @app.route("/", methods=["POST"])
    def receiver() -> tuple[str, int]:
        ms_info: list[str] = request.json["microservice"]
        log_report(ms_info[0], ms_info[1], request.json["chat_id"])
        
        sender.send(request.json)
        
        return "OK", 202
    
    return app
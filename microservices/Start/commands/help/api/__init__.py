# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    API.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import threading

from flask import Flask, request
from typing import Union

from .config.paths import LogSchema
from .connections.send_log import SendToLog

from .services.respond_client import RespondClient
# |--------------------------------------------------------------------------------------------------------------------|


def create_app(test_config: Union[bool, None] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping()
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    
    # POST ROUTE CONFIG |----------------------------------------------------------------------------------------------|
    def log_report(chat_id: str) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_from_start_driver"]
        threading.Thread(
            target=SendToLog().report,
            args=(log_schema[0], log_schema[1], chat_id)
        ).start()
        
        respond_client: RespondClient = RespondClient()
        
        @app.route("/", methods=["POST"])
        def receiver() -> tuple[str, int]:
            log_report(request.json["chat_id"])
            
            threading.Thread(
                target=respond_client.post,
                args=(request.json,)
            ).start()
            
            return "OK", 202
    # |----------------------------------------------------------------------------------------------------------------|
    
    return app
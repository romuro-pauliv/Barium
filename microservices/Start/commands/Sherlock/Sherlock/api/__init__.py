# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    api.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Flask, request
from typing import Union
import threading

from .services.request_data import RequestUserData

from .connections.send_log import SendToLog
from .config.paths import LogSchema
# |--------------------------------------------------------------------------------------------------------------------|


def create_app(test_config: Union[bool, None] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping()
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # HOME ENDPOINT |--------------------------------------------------------------------------------------------------|
    def log_report(chat_id) -> None:
        log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["received_message_start_driver"]
        threading.Thread(
            target=SendToLog().report,
            args=(log_schema[0], log_schema[1], chat_id)
        ).start()
    
    @app.route("/", methods=["POST"])
    def receiver() -> tuple[str, int]:
        chat_id: str = request.json["chat_id"]
        request_user_data = RequestUserData()
        
        log_report(chat_id)
        
        threading.Thread(
            target=request_user_data.send,
            args=(chat_id, )
        ).start()
        
        return "OK", 202
    # |----------------------------------------------------------------------------------------------------------------|
    
    from .routes.inform_username import bp_inform_username
    app.register_blueprint(bp_inform_username, url_prefix="/in-cache")
    
    from .routes.receiver_data_from_sherlock import bp_receiver_data_from_sherlock
    app.register_blueprint(bp_receiver_data_from_sherlock, url_prefix="/receiver-sherlock")
    
    return app
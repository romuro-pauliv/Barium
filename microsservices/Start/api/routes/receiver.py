# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.services.command_recognizer import Driver
import threading

# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("start", __name__)
driver: Driver = Driver()

@bp.route("/", methods=["POST"])
def message_receiver() -> tuple[str, int]:    
    
    threading.Thread(target=driver.direct_to, args=(request.json,)).start()
    
    return "OK", 202
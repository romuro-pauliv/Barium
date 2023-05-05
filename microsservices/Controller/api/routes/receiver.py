# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.controller.direct_path import driver
import threading
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("controller", __name__)

@bp.route("/", methods=["POST"])
def message_receiver() -> tuple[str, int]:    
    
    driver_task = threading.Thread(target=driver, args=(request.json, ))
    driver_task.start()
    
    return "OK", 202
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request

from api.controller.driver import Driver

from api.threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

bp: Blueprint = Blueprint("controller", __name__)

driver: Driver = Driver()

@bp.route("/", methods=["POST"])
def receiver() -> tuple[str, int]:
    Threads().start_thread(driver.drive, request.json)
    return "Accepted", 202
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request

from api.services.driver import Driver

from api.threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

driver: Driver = Driver()
threads: Threads = Threads()

bp: Blueprint = Blueprint('start', __name__)


@bp.route('/', methods=["POST"])
def receiver() -> tuple[str, str]:
    threads.start_thread(driver.driver, request.json)
    return "Accepted", 202
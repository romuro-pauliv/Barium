# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.routes.receiver.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request

from api.services.reply import Reply

from api.threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

reply: Reply = Reply()
threads: Threads = Threads()
bp: Blueprint = Blueprint("null", __name__)


@bp.route("/", methods=["POST"])
def receiver() -> tuple[str, str]:
    threads.start_thread(reply.client_responder, request.json)
    return "Accepted", 202
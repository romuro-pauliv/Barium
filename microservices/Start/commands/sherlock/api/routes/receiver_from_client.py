# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 api.routes.receiver_from_client.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request

from api.services.request_data import RequestInitData, RequestUsername

from api.threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

threads: Threads = Threads()
request_init_data: RequestInitData = RequestInitData()
request_username: RequestUsername = RequestUsername()
bp: Blueprint = Blueprint("receiver-from-client", __name__)


@bp.route("/", methods=["POST"])
def receiver_command() -> tuple[str, int]:
    threads.start_thread(request_init_data.client_responder, request.json)
    return "Accepted", 202


@bp.route("/username", methods=["POST"])
def receiver_username() -> tuple[str, int]:
    threads.start_thread(request_username.client_responder, request.json)
    return "Accepted", 202
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     api.routes.data_from_client.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import request, Blueprint

from api.services.data_from_client import DataFromClient
from api.threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

threads: Threads = Threads()
data_from_client: DataFromClient = DataFromClient()
data_from_client.schema()

bp_data_from_client: Blueprint = Blueprint("data-from-client", __name__)


@bp_data_from_client.route("/", methods=['POST'])
def data_receiver() -> tuple[str, int]:
    threads.start_thread(data_from_client.post, request.json)
    return "Accepted", 202

@bp_data_from_client.route("/", methods=["GET"])
def get_data() -> tuple[str, int]:
    return data_from_client.get(), 200

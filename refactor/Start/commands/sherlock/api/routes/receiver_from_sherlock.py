# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               API.routes.receiver_from_sherlock.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.services.receiver_data_sherlock import ReceiverDataSherlock
# |--------------------------------------------------------------------------------------------------------------------|

receiver_data_sherlock: ReceiverDataSherlock = ReceiverDataSherlock()
bp_receiver_data_from_sherlock: Blueprint = Blueprint("receiver_data_from_sherlock", __name__)


@bp_receiver_data_from_sherlock.route("/", methods=["POST"])
def receiver() -> tuple[str, int]:
    receiver_data_sherlock.sherlock_processing(request.json)
    return "Created", 201
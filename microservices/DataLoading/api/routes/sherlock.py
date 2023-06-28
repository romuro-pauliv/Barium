# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             api.routes.sherlock.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request

from api.services.sherlock import Sherlock

from api.threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

threads: Threads = Threads()

sherlock: Sherlock = Sherlock()
sherlock.schema_to_targets()

bp_sherlock: Blueprint = Blueprint("sherlock", __name__)


@bp_sherlock.route("/post-target", methods=["POST"])
def post_sherlock_target() -> tuple[str, int]:
    threads.start_thread(sherlock.post_username_target, request.json)
    return "Accepted", 202


@bp_sherlock.route("/get-target", methods=["GET"])
def get_sherlock_target() -> tuple[dict[str, str], int]:
    return sherlock.get_target(request.json), 200
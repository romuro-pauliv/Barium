# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          api.routes.get_session.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint
from api.services.session.handling_session import Session
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("session", __name__)

# Service Class
session = Session()

@bp.route("/", methods=["GET"])
def get_session() -> tuple[list[str], int]:
    return session.get(), 201
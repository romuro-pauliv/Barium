# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              api.routes.session.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint

from api.services.generate_session import GenerateSession
# |--------------------------------------------------------------------------------------------------------------------|

bp: Blueprint = Blueprint("session", __name__)

generate_session: GenerateSession = GenerateSession()

@bp.route("/", methods=["GET"])
def get_session() -> tuple[list[str], int]:
    return generate_session.get(), 200
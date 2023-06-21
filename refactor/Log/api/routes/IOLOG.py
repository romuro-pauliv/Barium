# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               api.routes.IOLOGS.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.log.logging_format import logger
import threading
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("logs", __name__)

@bp.route("/debug", methods=["POST"])
def debug_post() -> tuple[str, int]:
    
    msg_to_log: str = request.json["report"]
    d: dict[str, str] = request.json["extra"]
    
    logger.debug(msg_to_log, extra=d)
    
    return "Created", 201


@bp.route("/info", methods=["POST"])
def info_post() -> tuple[str, int]:
    
    msg_to_log: str = request.json["report"]
    d: dict[str, str] = request.json["extra"]
    
    logger.info(msg_to_log, extra=d)
    
    return "Created", 201


@bp.route("/warning", methods=["POST"])
def warning_post() -> tuple[str, int]:
    
    msg_to_log: str = request.json["report"]
    d: dict[str, str] = request.json["extra"]
    
    logger.warning(msg_to_log, extra=d)
    
    return "Created", 201


@bp.route("/error", methods=["POST"])
def error_post() -> tuple[str, int]:
    
    msg_to_log: str = request.json["report"]
    d: dict[str, str] = request.json["extra"]
    
    logger.error(msg_to_log, extra=d)
    
    return "Created", 201


@bp.route("/critical", methods=["POST"])
def critical_post() -> tuple[str, int]:
    
    msg_to_log: str = request.json["report"]
    d: dict[str, str] = request.json["extra"]
    
    logger.critical(msg_to_log, extra=d)
    
    return "Created", 201
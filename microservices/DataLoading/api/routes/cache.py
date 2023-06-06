# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           api.routes.post_cache.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.cache.redis_connect import Cache

import threading

from api.config.paths import LogSchema
from api.connections.send_log import SendToLog
# |--------------------------------------------------------------------------------------------------------------------|

bp_cache = Blueprint("cache", __name__)


def log_report(chat_id: str) -> None:
    log_schema: list[str] = LogSchema.LOG_REPORT_MSG["connections"]["send_cache_to_redis"]
    threading.Thread(
        target=SendToLog().report,
        args=(log_schema[0], log_schema[1], chat_id)
    ).start()
    

@bp_cache.route("/db0", methods=["POST"])
def post_cache() -> tuple[str, int]:
    chat_id: str = request.json["chat_id"]
    cache_value: str = request.json["cache_value"]
    
    Cache.TalkMode.db0_cache.mset({chat_id: cache_value})
    
    return "OK", 202

@bp_cache.route("/db0", methods=["DELETE"])
def delete_cache() -> tuple[str, int]:
    chat_id: str = request.json["chat_id"]
    
    Cache.TalkMode.db0_cache.delete(chat_id)
    
    return "OK", 202
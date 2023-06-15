# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                            api.routes.cache_db0.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request

from api.connections.cache import CacheDB, CacheConnect
# |--------------------------------------------------------------------------------------------------------------------|

bp_cachedb0: Blueprint = Blueprint("cache", __name__)

cache_connect: CacheConnect = CacheConnect(CacheDB.db0)


@bp_cachedb0.route("/db0", methods=["POST"])
def post_cache() -> tuple[str, int]:
    chat_id: str = request.json['chat_id']
    cache_value: str = request.json['cache_value']
    
    cache_connect.post(chat_id, cache_value)
    
    return "Created", 201


@bp_cachedb0.route("/db0", methods=["DELETE"])
def delete_cache() -> tuple[str, int]:
    chat_id: str = request.json["chat_id"]
    
    cache_connect.delete(chat_id)
    
    return "Created", 201
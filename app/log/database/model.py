# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          app.log.database.model.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import datetime
from typing import Union
# |--------------------------------------------------------------------------------------------------------------------|

def log(chat_id: str, username: str, log_key: str) -> dict[str, Union[str, datetime.datetime]]:
    return {
        "datetime": datetime.datetime.utcnow(),
        "chat_id": chat_id,
        "username": username,
        "log": log_key
    }
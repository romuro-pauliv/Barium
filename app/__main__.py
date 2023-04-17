# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Any
from time import sleep
from cache.redis_connect import Cache
from cache.load.login_db import loading_user_in_cache
from core.messages.schema import FIRST_EXEC, LOGIN_EXEC
from log.terminal.messages import MessagesLog
from core.tools.threading_mode import run_in_background
# |--------------------------------------------------------------------------------------------------------------------|

from core.telegram import Telegram
Telegram_ = Telegram()
loading_user_in_cache()


while True:
    last_message: dict[str, dict[str, Any]] = Telegram_.last_message()
    if last_message:
        for id_ in last_message.keys():
            data: dict[str, str] = last_message[id_]
            data["chat_id"] = str(id_)
            
            run_in_background(MessagesLog.received_message, (data["chat_id"], data["text"], ))
            
            if Cache.TalkMode.log_in_branch.get(str(id_)):
                if Cache.TalkMode.add_wallet_branch.get(str(id_)):
                    LOGIN_EXEC.add_wallet_command(data)
                    continue
                LOGIN_EXEC.first_commands(data)
                continue
            
            if Cache.TalkMode.open_account_branch.get(str(id_)):
                FIRST_EXEC.open_account_command(id_, data)
                continue
            
            FIRST_EXEC.first_commands(data)
            sleep(0.1)
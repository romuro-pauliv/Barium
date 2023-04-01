# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

from typing import Any
from core.tools.threading_mode import run_in_background

from core.telegram import Telegram
Telegram_ = Telegram()

from views.start.start.exec_ import StartChatExec
StartChatExec_ = StartChatExec()


while True:
    last_message: dict[str, dict[str, Any]] = Telegram_.last_message()
    if last_message:
        for id_ in last_message.keys():
            data: dict[str, str] = last_message[id_]
            data["chat_id"] = id_
            
            run_in_background(StartChatExec_.exec_, (data,))
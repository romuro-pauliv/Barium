# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from services.telegram.get_message import Core
from services.controller.post_data import PostController

from connections.log import LogConnect

from resources.data import TELEGRAM_API

from threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

core: Core = Core()
log_connect: LogConnect = LogConnect()
post_controller: PostController = PostController()
therads: Threads = Threads()

while True:
    last_message: dict[str, dict[str, str]] = core.last_message()
    if last_message:
        for id_ in last_message.keys():
            
            data: int = last_message[id_]
            data["chat_id"] = str(id_)
            
            therads.start_thread(log_connect.report, "get", TELEGRAM_API['uri'], "info", str(id_), True)
            therads.start_thread(post_controller.send, data)
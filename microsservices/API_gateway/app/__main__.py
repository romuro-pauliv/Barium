# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from core.last_message import Core
from connections.send_controller import SendToController
import threading
# |--------------------------------------------------------------------------------------------------------------------|

core = Core()

while True:
    last_message: dict[str, dict[str, str]] = core.last_message()
    if last_message:
        for id_ in last_message.keys():
            data = last_message[id_]
            data["chat_id"] = str(id_)
            
            # POST in controller API |---------------------------------------------------------------------------------|
            post_task: threading.Thread = threading.Thread(target=SendToController().post, args=(data,))
            post_task.start()
            # |--------------------------------------------------------------------------------------------------------|
            
            print(data)
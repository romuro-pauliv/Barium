# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    app.__main__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from core.last_message import Core
# |--------------------------------------------------------------------------------------------------------------------|

core = Core()

while True:
    last_message: dict[str, dict[str, str]] = core.last_message()
    if last_message:
        for id_ in last_message.keys():
            print(last_message[id_])
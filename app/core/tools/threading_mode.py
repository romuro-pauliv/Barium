# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   app.core.tools.threading_mode.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import threading
from typing import Callable, Any
# |--------------------------------------------------------------------------------------------------------------------|


def run_in_background(func: Callable[[dict[str, Any]], None], args: dict[str, Any]):
    thread = threading.Thread(target=func, args=args)
    thread.start()

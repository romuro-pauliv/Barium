# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          app.threads.executable.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import threading
from typing import Callable
# |--------------------------------------------------------------------------------------------------------------------|

class Threads(object):
    def __init__(self) -> None:
        pass
    
    def start_thread(self, func: Callable, *args, **kwargs) -> None:
        """
        Start a new thread to execute the given function with the provided arguments.
        Args:
            func (Callable): The function to be executed in the new thread.
            *args: Variable-length argument list for the function.
            **kwargs: Arbitrary keyword arguments for the function.
        """
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
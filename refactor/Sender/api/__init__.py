# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    api.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Flask, request

from .services.sender import Sender

from .threads.executable import Threads
# |--------------------------------------------------------------------------------------------------------------------|

sender: Sender = Sender()
threads: Threads = Threads()

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    
    @app.route("/", methods=["POST"])
    def receiver() -> tuple[str, int]:
        threads.start_thread(sender.send, request.json)
        return "Accepted", 202
            
    return app

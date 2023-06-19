# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    api.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Flask
# |--------------------------------------------------------------------------------------------------------------------|


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    
    from .routes.receiver_from_client import bp
    app.register_blueprint(bp, url_prefix="/sherlock")
    
    from .routes.receiver_from_sherlock import bp_receiver_data_from_sherlock
    app.register_blueprint(bp_receiver_data_from_sherlock, url_prefix="/receiver-sherlock")
    
    return app
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
    
    from .routes.receiver import bp
    app.register_blueprint(bp, url_prefix="/start")
    
    return app
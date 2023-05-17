# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    api.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Flask
from typing import Union
# |--------------------------------------------------------------------------------------------------------------------|


def create_app(test_config: Union[bool, None] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping()
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    
    # Blueprints |-----------------------------------------------------------------------------------------------------|
    from .routes.receiver import bp
    app.register_blueprint(bp, url_prefix="/start")
    # |----------------------------------------------------------------------------------------------------------------|
    
    return app

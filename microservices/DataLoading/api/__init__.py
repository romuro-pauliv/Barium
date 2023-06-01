# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    api.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Flask
from typing import Union
import os
from dotenv import load_dotenv
# |--------------------------------------------------------------------------------------------------------------------|


def create_app(test_config: Union[bool, None] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping()
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    from .routes.get_session import bp
    app.register_blueprint(bp, url_prefix="/session")
    
    from .routes.post_cache import bp_cache
    app.register_blueprint(bp_cache, url_prefix="/cache")
    
    return app
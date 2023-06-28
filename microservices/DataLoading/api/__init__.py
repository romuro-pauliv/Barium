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
    
    from .routes.session import bp
    app.register_blueprint(bp, url_prefix="/session")
    
    from .routes.cache_db0 import bp_cachedb0
    app.register_blueprint(bp_cachedb0, url_prefix="/cache")
    
    from .routes.sherlock import bp_sherlock
    app.register_blueprint(bp_sherlock, url_prefix="/sherlock")
    
    from .routes.data_from_client import bp_data_from_client
    app.register_blueprint(bp_data_from_client, url_prefix="/client-data")
    
    return app

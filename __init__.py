import logging
from flask import Flask
from flask_wtf import CSRFProtect
from config import Config
csrf = CSRFProtect()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    csrf.init_app(app)
    from .routes import main
    app.register_blueprint(main)
    return app

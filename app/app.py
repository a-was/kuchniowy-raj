from flask import Flask

from .config import Config
from . import db

__all__ = ['create_app']


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    init_blueprints(app)
    db.init_app(app)

    return app


def init_blueprints(application):
    from app.routes import app as main
    for blueprint in [main, ]:
        application.register_blueprint(blueprint)

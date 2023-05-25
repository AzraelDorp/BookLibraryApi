from flask import Flask
from shared.config import get_config
from app.blueprint import blueprint


def create_app():
    app = Flask(__name__)

    # get configuration
    config = get_config()
    app.config.from_mapping(config)

    # register blueprint
    app.register_blueprint(blueprint)

    return app
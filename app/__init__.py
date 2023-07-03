from flask import Flask
from .shared.config import get_config
from .blueprint import blueprint
import serverless_wsgi


def create_app():
    app = Flask(__name__)

    # get configuration
    # config = get_config()
    # app.config.from_mapping(config)

    # register blueprint
    app.register_blueprint(blueprint)
    return app


#     return app

# app = Flask(__name__)

# # # register blueprint
# app.register_blueprint(blueprint)

app = create_app()

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

def lambda_handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

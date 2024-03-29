from flask import Flask, request
from logging.config import dictConfig
from mongoengine import connect

from dub.resources import *


def init_api_auth(app):
    @api_blueprint.before_request
    def before_request():
        headers = request.headers
        if (
                ("Authorization" in headers
                 and headers["Authorization"] == f'Bearer {app.config["AUTH_TOKEN"]}')
                or request.endpoint.startswith("api.mojang_api")
                or request.endpoint.startswith("api.sa_launcher")
        ):
            return

        return "", 403


def create_app(config_filename):
    """Application factory."""

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.app_context().push()

    init_api_auth(app)
    
    # Connect to mongo
    connect(host=app.config["DB_URL"])

    # # Create media root
    # os.mkdir(app.config['MEDIA_ROOT'])

    app.register_blueprint(api_blueprint)
    app.register_blueprint(auth_server_blueprint)
    app.register_blueprint(root_blueprint)
    app.register_blueprint(session_server_blueprint)
    app.register_blueprint(minecraft_services_blueprint)

    return app
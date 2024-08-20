import logging
import sys

from civis_app.views.errors import APIError
from flask import Flask, jsonify
from flask.logging import default_handler


def create_app():
    # We will service static files from the dist folder
    # Assumes the frontend is written in React and bundled by webpack
    _template_folder = "./dist"
    app = Flask(
        __name__,
        template_folder=_template_folder,
        static_folder=_template_folder,
        static_url_path="",
    )

    app.url_map.strict_slashes = False

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # This should be ./config/production.py
    # and is set in the Dockerfile
    app.config.from_envvar("APP_CONFIG_FILE")

    register_blueprints(app)
    register_error_handlers(app)
    configure_logger(app)
    return app


def register_blueprints(app):
    from civis_app.views.api import api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    from civis_app.views.root import root_blueprint

    app.register_blueprint(root_blueprint)


def register_error_handlers(app):
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app.errorhandler(APIError)(handle_api_error)


def configure_logger(app):
    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    app.logger.removeHandler(default_handler)
    app.logger.setLevel(logging.INFO)

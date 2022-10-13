from flask import Blueprint

api_blueprint = Blueprint("api_blueprint", __name__)

from civis_app.views.api import fruit

__all__ = ["fruit"]

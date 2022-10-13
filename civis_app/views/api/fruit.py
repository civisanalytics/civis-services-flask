import os

from civis_app.views.api import api_blueprint
from flask import jsonify

import civis

# Initialization run on startup of each worker
service_username = None
if os.environ.get("CIVIS_API_KEY"):
    print("Retrieving username from API", flush=True)
    # The `CIVIS_API_KEY` environment variable here is that of whoever owns
    # the service This is true everywhere in this Flask application Hence
    # the API client below is running on behalf of whoever owns the service
    client = civis.APIClient()
    service_username = client.username


# Create your own API endpoints here
@api_blueprint.route("/fruits", methods=["GET"])
def list_fruits():
    favorite_fruit = os.environ.get("FLASK_DEMO_FAVORITE_FRUIT_PASSWORD")

    data = [
        {
            "name": "Strawberry",
            "number": 1,
        },
        {
            "name": "Watermelon",
            "number": 2,
        },
        {
            "name": "Grapefruit",
            "number": 3,
        },
        {
            "name": service_username,
            "number": 4,
        },
    ]
    for f in data:
        f["is_favorite"] = f["name"] == favorite_fruit

    return jsonify(data), 200


@api_blueprint.route("/health", methods=["GET"])
def healthcheck():
    service_id = os.environ.get("CIVIS_SERVICE_ID")
    if service_id is None:
        return "This service is running locally.", 200

    return f"The ID of this service is: {service_id}", 200

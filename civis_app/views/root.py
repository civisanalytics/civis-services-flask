from flask import Blueprint, render_template

_TEMPLATE_FILE = "index.html"

root_blueprint = Blueprint("root_blueprint", __name__)


@root_blueprint.route("/")
def index():
    return render_template(_TEMPLATE_FILE)


# Here we define your own custom status endpoint
# Platform will continuously hit this endpoint to make sure your service
# is still up, since we've defined this endpoint via the
# `CIVIS_SERVICE_HEALTH_PATH` environment variable.
# Otherwise, it will use the root endpoint (/)
# If your app connects to a database, it is common to do a `SELECT 1`
# and make sure that succeeds
@root_blueprint.route("/status")
def health_check():
    # For purposes of a demo, just always return 200
    return "App is up", 200

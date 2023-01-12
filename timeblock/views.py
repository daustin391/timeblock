"""
Module for handling requests to the web server.

Constants:
    ROUTES - Blueprint object for registering URL routes with application.

The following functions are defined:
    index_get - Handles GET requests to root path.
        Returns rendered HTML template.
    index_post - Handles POST requests to root.
        Inserts form data into database.
"""
from flask import render_template, request, redirect, Blueprint, current_app
from werkzeug.wrappers.response import Response

from timeblock import sql
from timeblock.action import Action

ROUTES = Blueprint("routes", __name__)


@ROUTES.route("/", methods=["POST"])
def index_post() -> Response:
    """
    Handle POST requests to root path.

    Writes action to database and redirects to root path.

    Returns:
        Response: Werkzeug response object redirecting to root.
    """
    action = request.form["action"]
    action_obj = Action(action)

    with sql.TimeblockDB(current_app.config["DATABASE"]) as database:
        database.add_action(action_obj)
    return redirect("/")


@ROUTES.route("/", methods=["GET"])
def index_get() -> str:
    """
    Handle GET requests to root path.

    Checks database for actions and renders template with them.

    Returns:
        str: Rendered HTML template for the main page.
    """
    with sql.TimeblockDB(current_app.config["DATABASE"]) as database:
        actions = database.read_query("SELECT * FROM action")

    context: dict = {
        "actions": [Action.from_tuple(action) for action in actions]
    }
    return render_template("actions.html", actions=context["actions"])

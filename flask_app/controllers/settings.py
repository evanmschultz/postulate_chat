from werkzeug import Response
from flask_app import app

from flask_app import app, socketio
from flask import jsonify, render_template, request, redirect, session, flash, url_for

from flask_app.models.user import User
from flask_app.models.chat import Chat

from flask_app.controllers.route_utilities import is_user_logged_in
from flask_app.services.ingestion_manager import IngestionManager
from flask_app.services.vector_database import VectorDatabase


@app.route("/settings", methods=["GET"])
def settings_menu() -> Response | str:
    """
    Settings menu where users can update their information.

    Checks if the user is logged in. If not, redirects to the login page.
    Otherwise, serves the settings menu to the user.

    Returns:
        Rendered HTML template or Redirect.
    """
    redirect_user: Response | None = is_user_logged_in()
    if redirect_user:
        return redirect_user

    user_id: int = session["user_id"]
    user_info: User = User.get_user_by_id(user_id)
    user_chats: list[Chat] = User.get_all_chats_by_user_id(user_id)

    settings: bool = True
    return render_template(
        "chat_interface.html",
        user_info=user_info,
        user_chats=user_chats,
        settings=settings,
    )


@app.route("/update_user_info", methods=["POST"])
def update_user_info():
    """
    Update User Information route.

    Gets the input data from the form and validates it using the `update_user_by_id` method
    in the User model. If validation fails, flashes error messages and redirects to the
    settings_menu route (or any route where the settings form resides).
    Otherwise, updates the user information in the database, and redirects to the settings_menu.

    Returns:
        Redirect: Redirects to the settings_menu if the update is successful, or back to the settings_menu
        if validation fails.
    """
    # Ensure the user is logged in before proceeding
    redirect_user = is_user_logged_in()
    if redirect_user:
        return redirect_user

    # Get user ID from session
    user_id = session["user_id"]

    # Get form data
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
    }

    # Validate and update user information
    if not User.update_user_by_id(user_id, data):
        flash("Failed to update user information. Please try again.", "error")
        return redirect(url_for("settings_menu"))

    flash("Successfully updated user information.", "update_success")
    return redirect(url_for("settings_menu"))


# TODO: Update to use user_id from session for VectorDatabase
@app.route("/ingest_single_url", methods=["POST"])
def ingest_single_url():
    print(
        f"""\n{'_'*80}
        \nroute called\n
        \n{'_'*80}
        """
    )
    data = request.json
    url = data.get("url")  # type: ignore
    ingestion_manager = IngestionManager()
    vector_database = VectorDatabase()

    if url is None:
        return jsonify({"error": "URL is missing"}), 400

    try:
        ingestion_manager.ingest_single_url(url, vector_database)
        print(
            f"""\n{'_'*80}
            \ningestion try block\n
            \n{'_'*80}
            """
        )
        return jsonify({"message": f"Successfully ingested {url}"}), 200
    except Exception as e:
        print(
            f"""\n{'_'*80}
            \ningestion except block\n
            \n{'_'*80}
            """
        )
        return jsonify({"error": str(e)}), 500


# TODO: Update to use user_id from session for VectorDatabase
@app.route("/ingest_urls", methods=["POST"])
def ingest_urls_route():
    print(
        f"""\n{'_'*80}
        \nurls called\n
        \n{'_'*80}
        """
    )
    data = request.json
    urls = data.get("urls")  # type: ignore
    ingestion_manager = IngestionManager()
    vector_database = VectorDatabase()

    if urls is None:
        return jsonify({"error": "URLs are missing"}), 400

    try:
        ingestion_manager.ingest_urls(urls, vector_database)
        return jsonify({"message": "Successfully ingested URLs"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

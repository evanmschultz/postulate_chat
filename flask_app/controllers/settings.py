from werkzeug import Response
from flask_app import app

from flask_app import app, socketio
from flask import jsonify, render_template, request, redirect, session, flash, url_for

from flask_app.models.user import User
from flask_app.models.chat import Chat
from flask_app.models.message import Message
from flask_app.controllers.route_utilities import is_user_logged_in


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

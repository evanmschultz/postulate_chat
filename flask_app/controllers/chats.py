from flask_app import app

from flask_app import app, socketio
from flask import render_template, request, redirect, session, flash, url_for


@app.route("/chat", methods=["GET"])
def chat_interface():
    """
    Chat interface where users interact with the AI.

    Checks if the user is logged in. If not, redirects to the login page.
    Otherwise, serves the chat interface to the user.

    Returns:
        Rendered HTML template or Redirect.
    """
    if not is_user_logged_in():
        flash("Please login or register to enter the chat.", "login_error")
        return redirect(url_for("login_page"))
    return render_template("chat_interface.html")


@app.route("/settings", methods=["GET"])
def settings_menu():
    """
    Settings menu where users can update their information.

    Checks if the user is logged in. If not, redirects to the login page.
    Otherwise, serves the settings menu to the user.

    Returns:
        Rendered HTML template or Redirect.
    """
    if not is_user_logged_in():
        flash("Please login or register to access settings.", "login_error")
        return redirect(url_for("login_page"))
    return render_template("settings.html")


@app.route("/settings/update_name", methods=["POST"])
def update_name():
    """
    Update user name.

    Checks if the user is logged in and then updates the name.

    Returns:
        Redirect: Redirects to the settings menu.
    """
    # TODO: Add necessary logic
    return redirect("/settings")


@app.route("/settings/update_email", methods=["POST"])
def update_email():
    """
    Update user email.

    Checks if the user is logged in and then updates the email.

    Returns:
        Redirect: Redirects to the settings menu.
    """
    # TODO: Add necessary logic
    return redirect("/settings")


@app.route("/settings/update_password", methods=["POST"])
def update_password():
    """
    Update user password.

    Checks if the user is logged in and then updates the password.

    Returns:
        Redirect: Redirects to the settings menu.
    """
    # TODO: Add necessary logic
    return redirect("/settings")


@app.route("/settings/delete_account", methods=["POST"])
def delete_account():
    """
    Delete user account.

    Checks if the user is logged in and then deletes the account.

    Returns:
        Redirect: Redirects to the home page.
    """
    # TODO: Add necessary logic
    return redirect("/")


@app.route("/chat/update_thread_name", methods=["POST"])
def update_thread_name():
    """
    Update the name of the chat thread.

    Checks if the user is logged in and then updates the thread name.

    Returns:
        Redirect: Redirects to the chat interface.
    """
    # TODO: Add necessary logic
    return redirect("/chat")


@app.route("/chat/delete_thread", methods=["POST"])
def delete_thread():
    """
    Delete a chat thread.

    Checks if the user is logged in and then deletes the chat thread.

    Returns:
        Redirect: Redirects to the chat interface.
    """
    # TODO: Add necessary logic
    return redirect("/chat")


@app.route("/chat/upload", methods=["POST"])
def upload_document():
    """
    Upload a document or URL.

    Checks if the user is logged in and then uploads the document or URL.

    Returns:
        Redirect: Redirects to the chat interface.
    """
    # TODO: Add necessary logic
    return redirect("/chat")


# Utility functions
def is_user_logged_in():
    """
    Checks if a user is logged in by verifying if "user_id" exists in the session.

    Returns:
        bool: True if the user is logged in, otherwise False.
    """
    return "user_id" in session

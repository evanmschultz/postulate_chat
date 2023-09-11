from flask_app import app

from flask_app.models.user import User
from flask import render_template, request, redirect, session, flash, url_for


@app.route("/", methods=["GET"])
def login_page():
    """Login or Register as a user"""
    return render_template("login_page.html")


@app.route("/register", methods=["POST"])
def register():
    """
    Register user route.

    Gets the input data from the form and validates it using the validate_user method
    in the User model. If validation fails, flashes error messages and redirects to the
    login_page route. Otherwise, registers the user in the database, stores the user's
    ID and first name in session, and redirects to the chat.

    Returns:
        Redirect: Redirects to the chat page if registration is successful, or the
            login_page route if validation fails.
    """
    data: dict = dict(request.form)
    if not User.validate_user(data):
        return redirect(url_for("login_page"))

    user_id: int = User.register_user(data)
    user_first_name: str = data["first_name"]
    session["user_id"], session["user_first_name"] = user_id, user_first_name
    return redirect("/chat")


@app.route("/login", methods=["POST"])
def login():
    """
    Login a user route.

    Checks for a user in the database with the input email and password. If the email
    is not in the database or the hashed_password doesn't match that user's password
    in the database, flashes error message and redirects to the login_page route. Otherwise,
    gets the user_id and user_first_name from the database, stores them in session, then redirects
    to the chat.

    Returns:
        Redirect: Redirects to the chat page if successful, or the login_page route if the
            email is not in the database or the password doesn't match.
    """
    data: str = request.form["email"]
    user_in_db: User | None = User.get_user_by_email(data)

    if not user_in_db or not User.check_password(
        user_in_db.password, request.form["password"]  # type: ignore
    ):
        flash("Invalid Email and/or Password", "login_error")
        return redirect(url_for("login_page"))

    user_id: int = user_in_db.id  # type: ignore
    user_first_name: str = user_in_db.first_name  # type: ignore
    session["user_id"], session["user_first_name"] = user_id, user_first_name

    return redirect("/chat")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Logout route.

    Clears session and redirects to the login_page route.
    """
    session.clear()
    return redirect("/")

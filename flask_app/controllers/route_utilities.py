from werkzeug import Response

from flask import redirect, session, flash, url_for


def is_user_logged_in() -> Response | None:
    """
    Checks if a user is logged in by verifying if "user_id" exists in the session.

    If the user is logged in ("user_id" exists in the session), returns a tuple with
    True and None. If the user is not logged in, flashes an error message and returns a tuple
    with False and a redirection to the login page.

    Returns:
        tuple: A tuple containing a boolean value representing whether the user is logged in,
               and either None (if logged in) or a redirect response (if not logged in).
    """
    if "user_id" not in session:
        flash("Please login or register to enter the site.", "login_error")
        return redirect(url_for("login_page"))

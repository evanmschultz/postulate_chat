from werkzeug import Response
from flask_app import app

from flask_app import app, socketio
from flask import jsonify, render_template, request, redirect, session, flash, url_for

from flask_app.models.user import User
from flask_app.models.chat import Chat
from flask_app.models.message import Message
from flask_app.controllers.route_utilities import is_user_logged_in


@app.route("/chat", defaults={"chat_id": None}, methods=["GET", "POST"])
@app.route("/chat/<int:chat_id>", methods=["GET", "POST"])
def chat_interface(chat_id: int | None) -> Response | str:
    """
    Handles the chat interface, including chat history and user chat IDs.

    Args:
        chat_id (int | None): The ID of the chat to be displayed. Defaults to None.

    Returns:
        Response | str: Renders the chat interface template with the chat history and chat IDs.
    """
    redirect_user: Response | None = is_user_logged_in()
    if redirect_user:
        return redirect_user

    user_id: int = session["user_id"]

    if chat_id:
        session["current_chat_id"] = chat_id
    elif session.get("current_chat_id"):
        chat_id = session["current_chat_id"]
    else:
        chat_id = Chat.create_new_chat(user_id)
        session["current_chat_id"] = chat_id

    chat: Chat = Chat.get_chat_by_id(chat_id)
    if not chat:
        # flash("Chat not found.", "error")
        print(f"{'_'*80}\n\nChat not found.\n\n{'_'*80}")
        chat_id = Chat.create_new_chat(user_id)
        chat: Chat = Chat.get_chat_by_id(chat_id)

    chat_history: list[Message] = chat.get_messages()

    user_chats: list[Chat] = User.get_all_chats_by_user_id(user_id)
    user_info: User = User.get_user_by_id(user_id)

    return render_template(
        "chat_interface.html",
        user_info=user_info,
        chat_history=chat_history,
        user_chats=user_chats,
        chat_id=chat_id,
    )


@app.route("/chat/ajax_send_message", methods=["POST"])
def ajax_send_message() -> Response:
    """
    Handles AJAX request for sending a chat message.

    Returns:
        Response: JSON response containing the bot's reply and the user's input.
    """
    redirect_user: Response | None = is_user_logged_in()
    if redirect_user:
        return redirect_user
    chat_id: int = int(request.form.get("chat_id"))  # type: ignore
    user_id: int = session["user_id"]
    if not chat_id:
        flash("Chat not found.", "error")
        return jsonify({"status": "error", "message": "Chat not found"})

    if not user_id == Chat.get_chat_by_id(chat_id).user_id:
        flash("Unauthorized.", "error")
        return jsonify({"status": "error", "message": "Unauthorized"})

    user_query: str = request.form.get("chat-input")  # type: ignore
    answer: str | None = Chat.generate_ai_response(chat_id, user_query)

    return jsonify({"bot_response": answer, "user_input": user_query})


@app.route("/chat/delete/<int:chat_id>", methods=["POST"])
def delete_chat(chat_id: int) -> Response:
    """
    Deletes a chat by its ID and redirects the user to another chat interface.

    Args:
        chat_id (int): The ID of the chat to be deleted.

    Returns:
        Response: Redirects to another chat interface, flashes a message based on the deletion status.
    """
    redirect_user: Response | None = is_user_logged_in()
    if redirect_user:
        return redirect_user

    deletion_success: bool = Chat.delete_chat_by_id(chat_id)

    if not deletion_success:
        flash("Failed to delete chat.", "error")
        return redirect(url_for("chat_interface"))

    user_id: int = session["user_id"]
    user_chat_ids: list[int] = User.get_all_chat_ids_by_user_id(user_id)
    if not user_chat_ids:
        next_chat_id = None
    else:
        next_chat_id = user_chat_ids[-1]

    return redirect(url_for("chat_interface", chat_id=next_chat_id))


@app.route("/chat/update_name", methods=["POST"])
def update_chat_name() -> Response:
    """
    Handles the updating of the chat name via POST request.

    This function checks if the user is authorized to update the chat name,
    then updates the chat name based on the user's input.

    Returns:
        Response: Redirects to the settings page and flashes a message indicating the
                  success or failure of the chat name update.
    """
    redirect_user: Response | None = is_user_logged_in()
    if redirect_user:
        return redirect_user

    chat_id: int = int(request.form.get("chat_id"))  # type: ignore

    new_chat_name: str = request.form.get("new_chat_name")  # type: ignore

    user_id: int = session["user_id"]
    if not user_id == Chat.get_chat_by_id(chat_id).user_id:
        flash("Unauthorized to update chat name.", "error")
        return redirect("/settings")

    update_success: bool = Chat.update_chat_name_by_id(chat_id, new_chat_name)
    if not update_success:
        flash("Failed to update chat name.", "error")

    return redirect("/settings")

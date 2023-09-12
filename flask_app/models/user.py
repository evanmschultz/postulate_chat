from datetime import datetime
from flask import flash
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_app.config.config import database
from pydantic import ValidationError
from flask_app.models.user_validation import UserData
from flask_app import database
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, joinedload
from flask_app.models.chat import Chat
from flask_app.services.vector_database import VectorDatabase


# TODO: Make methods in better accordance with SQLAlchemy ORM
# TODO: Update schema to allow full CRUD operations
class User(database.Model):
    """
    The User class is a model for storing user information and includes methods
    for hashing passwords, checking passwords, and handling user registration.
    """

    __tablename__: str = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)  # type: ignore
    first_name: str = Column(String(255))  # type: ignore
    last_name: str = Column(String(255))  # type: ignore
    email: str = Column(String(255), unique=True)  # type: ignore
    password: str = Column(String(255))  # type: ignore

    created_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Column[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship to Chat
    chats = relationship("Chat", back_populates="user")

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the given password using bcrypt and returns the hashed password.

        Args:
            password (str): The plain-text password to hash.

        Returns:
            str: The hashed password.
        """
        hashed_password: str = generate_password_hash(password).decode("utf-8")
        return hashed_password

    @staticmethod
    def check_password(hashed_password: str, password: str) -> bool:
        """
        Compares a hashed password with a plain-text password to check for a match.

        Args:
            hashed_password (str): The hashed password.
            password (str): The plain-text password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return check_password_hash(hashed_password, password)

    @classmethod
    def get_user_by_email(cls, email: str) -> "User":
        """
        Fetches a user from the database by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            User: User object if found, None otherwise.
        """
        return cls.query.filter_by(email=email).first()  # type: ignore

    @classmethod
    def get_user_by_id(cls, user_id: int) -> "User":
        """
        Fetches a user from the database by their user ID.

        Args:
            user_id (int): The user ID to search for.

        Returns:
            User: User object if found, None otherwise.
        """
        return cls.query.get(user_id)  # type: ignore

    @classmethod
    def get_all_chat_ids_by_user_id(cls, user_id) -> list[int]:
        """
        Fetches all chat IDs associated with a user from the database by their user ID.

        Args:
            user_id (int): The user ID to search for.

        Returns:
            list[int]: List of chat IDs if found, empty list otherwise.
        """
        user = cls.query.options(joinedload(cls.chats)).filter_by(id=user_id).first()
        if user is None:
            return []
        return [chat.id for chat in user.chats]

    # Do Not Use
    @classmethod
    def get_all_chats_by_user_id(cls, user_id: int) -> list[Chat]:
        """
        Fetches all the chats associated with a user from the database by their user ID.

        Args:
            user_id (int): The user ID to search for.

        Returns:
            list[Chat]: List of Chat objects if found, None otherwise.
        """
        return (
            cls.query.options(joinedload(cls.chats)).filter_by(id=user_id).first().chats  # type: ignore
        )

    @classmethod
    def register_user(cls, user_data: dict) -> int:
        """
        Registers a new user in the database using the provided user data.

        Args:
            user_data (dict): The data for the new user. Contains:
                {
                    'first_name': str,
                    'last_name': str,
                    'email': str,
                    'password': str
                }

        Returns:
            int: The ID of the newly registered user.
        """
        hashed_password = cls.hash_password(user_data["password"])
        new_user = cls(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=hashed_password,
        )  # type: ignore
        database.session.add(new_user)
        database.session.commit()
        return new_user.id  # type: ignore

    # TODO: Update for full CRUD operations
    @classmethod
    def update_user_by_id(cls, user_id: int, user_data: dict) -> bool:
        """
        Updates a user's first name, last name, and email by ID and validates the user's inputs before updating the database.

        Args:
            user_id (int): The ID of the user to update.
            user_data (dict): The data for the user to update. Contains:
                {
                    'first_name': str,
                    'last_name': str,
                    'email': str
                }

        Returns:
            bool: True if the user was updated, False otherwise.
        """
        if not cls.validate_user(user_data):
            return False

        user: User = cls.get_user_by_id(user_id)
        if not user:
            return False

        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.email = user_data["email"]

        database.session.commit()
        return True

    # TODO: Update for full CRUD operations
    @classmethod
    def update_password_by_id(
        cls, user_id: int, old_password: str, new_password: str
    ) -> bool:
        """
        Updates a user's password by ID after validating the old password.

        Args:
            user_id (int): The ID of the user to update.
            old_password (str): The old password to validate.
            new_password (str): The new password to set.

        Returns:
            bool: True if the password was updated, False otherwise.
        """
        user: User = cls.get_user_by_id(user_id)
        if not user:
            return False

        if not cls.check_password(user.password, old_password):
            flash("Old password is incorrect.", "update_error")
            return False

        try:
            UserData(
                password=new_password,
                confirm_password=new_password,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,  # type: ignore
            )
        except ValueError as e:
            flash(str(e), "update_error")
            return False

        hashed_new_password = cls.hash_password(new_password)

        user.password = hashed_new_password
        database.session.commit()

        return True

    @staticmethod
    def validate_user(user_data: dict) -> bool:
        """
        Validates user inputs using the Pydantic schema in the user_validation model and
        checks for email uniqueness.

        1. Extracts the email from the user_data.
        1. Validates the user_data using the Pydantic schema (UserData) and captures
        any validation errors.
        1. If validation errors are found, stores messages in flash_messages list and sets validation_passed
        to False.
        1. Checks if the email already exists in the database, if it does, appends a flash message to the
        flash_messages list and sets validation_passed to False.
        1. Runs loop to get set all flash messages from flash_messages list.

        If there were no validation errors, returns True.

        Args:
            user_data (dict): The user_data from the input form. Contains:
                {
                    'first_name': str,
                    'last_name': str,
                    'email': str,
                    'password': str,
                    'confirm_password': str
                }

        Returns:
            bool: True if validation checks pass and email is unique, False otherwise.

        Raises:
            Flash Message: ValueErrors from the UserData class and a message if
                email already exists.
        """
        user_email: str = user_data["email"]
        validation_passed = True
        flash_messages: list = []

        try:
            UserData(**user_data)
        except ValidationError as e:
            validation_passed = False

            for error in e.errors():
                if error["loc"][0] == "email":
                    flash_messages.append("Invalid email address.")
                else:
                    flash_messages.append(f"{error['msg'].strip('Value Error, ')}")

        if User.get_user_by_email(user_email):
            validation_passed = False
            flash_messages.append(
                "Email already exists. Login or use a different email."
            )

        for message in flash_messages:
            flash(message, "register_error")

        return validation_passed

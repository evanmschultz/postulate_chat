from datetime import datetime
from flask import flash
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_app.config.config import database
from pydantic import BaseModel, ValidationError
from flask_app.models.user_validation import UserData
from flask_app import database


class User(database.Model):
    __tablename__: str = "users"

    id: int = database.Column(database.Integer, primary_key=True, autoincrement=True)
    first_name: str = database.Column(database.String(255))
    last_name: str = database.Column(database.String(255))
    email: str = database.Column(database.String(255), unique=True)
    password: str = database.Column(database.String(255))

    created_at: datetime = database.Column(database.DateTime, default=datetime.utcnow)
    updated_at: datetime = database.Column(
        database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password: str = generate_password_hash(password).decode("utf-8")
        return hashed_password

    @staticmethod
    def check_password(hashed_password: str, password: str) -> bool:
        return check_password_hash(hashed_password, password)

    @classmethod
    def get_user_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_id(cls, user_id: int):
        return cls.query.get(user_id)

    @classmethod
    def register_user(cls, user_data: dict) -> int:
        hashed_password = cls.hash_password(user_data["password"])
        new_user = cls(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=hashed_password,
        )
        database.session.add(new_user)
        database.session.commit()
        return new_user.id

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

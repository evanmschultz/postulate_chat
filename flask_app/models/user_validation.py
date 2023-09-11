# from pydantic import BaseModel, EmailStr, FieldValidationInfo, field_validator
from pydantic import BaseModel, EmailStr, validator
import re

# TODO: Swap code for comments when Chroma updates to pydantic > 2.0.0

VALIDATION_RULES: dict = {
    "first_name": {
        "min_length": 2,
        "error_message": "First Name must be at least 2 characters.",
    },
    "last_name": {
        "min_length": 2,
        "error_message": "Last Name must be at least 2 characters.",
    },
    "password": {
        "min_length": 8,
        "regex": re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).+$"),
        "error_message": "Password must have 1 lowercase, 1 uppercase, 1 number, and 1 special character.",
    },
    "confirm_password": {"error_message": "The passwords must match."},
}


class UserData(BaseModel):
    """
    A Pydantic BaseModel class for user registration data validation.

    Pydantic's field_validator methods are used to enforce these rules. When an instance of this
    class is created, each field_validator method is called in sequence, creating a dictionary
    of values that can be accessed in later methods.

    The following class methods are used to validate the user's registration information:
    1. `validate_first_name`: Ensures the first_name is not empty.
    1. `validate_last_name`: Ensures the last_name is not empty.
    1. `validate_password`: Ensures the password meets complexity and length requirements.
    1. `validate_confirm_password`: Ensures that the password and confirm_password match.

    If any of the validations fail, a ValueError is thrown.
    """

    first_name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str

    # @field_validator("first_name")
    @validator("first_name")
    def validate_first_name(cls, value: str) -> str:
        """
        Ensures that the last_name field is not empty.

        Args:
            value (str): The first_name value.

        Returns:
            str: The validated first_name value.

        Raises:
            ValueError: If the first_name value is empty.
        """
        rule: dict = VALIDATION_RULES["first_name"]
        if len(value.strip()) < rule["min_length"]:
            raise ValueError(rule["error_message"])
        return value

    # @field_validator("last_name")
    @validator("last_name")
    def validate_last_name(cls, value: str) -> str:
        """
        Ensures that the last_name field is not empty.

        Args:
            value (str): The last_name value.

        Returns:
            str: The validated last_name value.

        Raises:
            ValueError: If the last_name value is empty.
        """
        rule = VALIDATION_RULES["last_name"]
        if len(value.strip()) < rule["min_length"]:
            raise ValueError(rule["error_message"])
        return value

    # @field_validator("password")
    @validator("password")
    def validate_password(cls, value: str) -> str:
        """
        Ensures the password meets complexity and length requirements.

        Checks the following criteria:
        1. Length: The password must be at least 8 characters long.

        1. Complexity: The password must contain at least 1 lowercase letter, 1 uppercase letter, 1
        number, and 1 special character using a regex.

        Args:
            value (str): The password string to be validated.

        Returns:
            str: The validated password string if it meets all requirements.

        Raises:
            ValueError: If the password does not meet the length or complexity requirements.
        """
        rule = VALIDATION_RULES["password"]
        if len(value.strip()) < rule["min_length"]:
            raise ValueError(rule["error_message"])
        if not rule["regex"].match(value):
            raise ValueError(rule["error_message"])
        return value

    @validator("confirm_password", pre=True, always=True)
    def validate_confirm_password(cls, value: str, values) -> str:
        """
        Ensures that the password and confirm_password match.

        If not a ValueError is thrown.

        Args:
            value (str): The confirm_password value to validate.
            values FieldValidationInfo: An instance of that class containing other previously validated
                                        field values.

        Returns:
            str: The validated confirm_password value.

        Raises:
            ValueError: If the confirm_password value does not match the password.
        """
        rule: dict = VALIDATION_RULES["confirm_password"]
        if "password" in values and values["password"] != value:
            raise ValueError(rule["error_message"])
        return value

    # @field_validator("confirm_password")
    # def validate_confirm_password(cls, value: str, values: FieldValidationInfo) -> str:
    #     """
    #     Ensures that the password and confirm_password match.

    #     If not a ValueError is thrown.

    #     Args:
    #         value (str): The confirm_password value to validate.
    #         values FieldValidationInfo: An instance of that class containing other previously validated
    #                                     field values.

    #     Returns:
    #         str: The validated confirm_password value.

    #     Raises:
    #         ValueError: If the confirm_password value does not match the password.
    #     """
    #     rule: dict = VALIDATION_RULES["confirm_password"]
    #     if "password" in values.data and values.data["password"] != value:
    #         raise ValueError(rule["error_message"])
    #     return value

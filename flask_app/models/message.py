from datetime import datetime
from pydantic import BaseModel, validator
from flask_app import database
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Message(database.Model):
    """
    Message model for storing individual chat messages.

    This class serves as the data model for chat messages in the database.
    It's designed to work with SQLAlchemy and is used to create, query, and manage individual chat messages in the DB.
    SQLAlchemy's ORM capabilities are used for database interaction. The `relationship` function is used to link
    this model to the Chat model, allowing for easy joins and queries.

    Attributes:
        id (Column[int]): Unique identifier for each message.
        content (Column[str]): The content of the message.
        message_type (Column[str]): Type of the message ('system_message', 'user_message', 'ai_message').
        created_at (Column[datetime]): The time the message was created.
        chat_id (Column[int]): Foreign key to the Chat model.
        chat (relationship): A relationship to the Chat model that this message belongs to.
    """

    __tablename__: str = "messages"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    content: Column[str] = Column(Text)
    message_type: Column[str] = Column(
        String(50)
    )  # 'system_message', 'user_message', 'ai_message'
    created_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    # Foreign key to Chat
    chat_id: Column[int] = Column(Integer, ForeignKey("chats.id"))

    # Relationship to Chat
    chat = relationship("Chat", back_populates="messages")

    @classmethod
    def add_message(cls, chat_id: int, content: str, message_type: str) -> None:
        print(f"\n{'_' * 80}\nAdding message to database...\n{'_' * 80}")
        new_message = cls(chat_id=chat_id, content=content, message_type=message_type)
        try:
            database.session.add(new_message)
            database.session.commit()
        except Exception as e:
            print(f"Error while saving message: {e}")


# TODO: Use schema for validation
class MessageSchema(BaseModel):
    """
    Pydantic schema for Message model.

    This class serves as the Pydantic schema for the Message model.
    It's useful for data validation and serialization when working with APIs.
    Pydantic's BaseModel is subclassed to create the schema.
    Each attribute is strongly typed to ensure data integrity.

    Attributes:
        id (int): Unique identifier for each message.
        content (str): The content of the message.
        message_type (str): Type of the message ('system_message', 'user_message', 'ai_message').
        created_at (datetime): The time the message was created.
        chat_id (int): Foreign key to the Chat model.
    """

    id: int
    content: str
    message_type: str
    created_at: datetime
    chat_id: int

    @validator("content", pre=True, always=True)
    def strip_and_validate_content(cls, value) -> str:
        """
        Strip and validate the 'content' field.

        This method is responsible for stripping leading and trailing whitespaces from the 'content'
        field and validating that the stripped value is not empty. It uses Pydantic's @validator
        decorator to perform this operation before any other validations.

        Args:
            value (str): The original 'content' value.

        Returns:
            str: The stripped 'content' value.

        Raises:
            ValueError: If the stripped 'content' is empty or consists only of whitespace.
        """
        stripped_value: str = value.strip()
        if not stripped_value:
            raise ValueError("Message content should not be empty or just whitespace.")
        return stripped_value

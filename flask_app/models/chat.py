from datetime import datetime
from pydantic import BaseModel
from flask_app import database
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship


class Chat(database.Model):
    """
    Chat model for storing chat sessions.

    This class serves as the data model for chat sessions in the database.
    It's designed to work with SQLAlchemy and is used to create, query, and manage chat sessions in the DB.
    SQLAlchemy's ORM capabilities are used for database interaction.The `relationship` function is used to
    link this model to the Message model, allowing for easy joins and queries.

    Attributes:
        id (Column[int]): Unique identifier for each chat.
        created_at (Column[datetime]): The time the chat was created.
        updated_at (Column[datetime]): The time the chat was last updated.
        session_id (Column[str]): A string representing the session ID.
        messages (relationship): A relationship to Message models that belong to this chat.
    """

    __tablename__: str = "chats"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Column[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    session_id: Column[str] = Column(String(50))

    # Relationship to Message
    messages = relationship("Message", back_populates="chat")


class ChatSchema(BaseModel):
    """
    Pydantic schema for Chat model.

    This class serves as the Pydantic schema for the Chat model.
    It's useful for data validation and serialization when working with APIs.
    Pydantic's BaseModel is subclassed to create the schema.
    Each attribute is strongly typed to ensure data integrity.

    Attributes:
        id (int): Unique identifier for each chat.
        created_at (datetime): The time the chat was created.
        updated_at (datetime): The time the chat was last updated.
        session_id (str): A string representing the session ID.
    """

    id: int
    created_at: datetime
    updated_at: datetime
    session_id: str

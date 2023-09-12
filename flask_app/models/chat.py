from datetime import datetime
from flask import flash
from pydantic import BaseModel, ValidationError, validator
from flask_app import database
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from sqlalchemy.orm import relationship
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from flask_app.services.vector_database import VectorDatabase
from flask_app.models.message import Message
from sqlalchemy.exc import SQLAlchemyError


# TODO: Make methods in better accordance with SQLAlchemy ORM
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    session_id = Column(String(50))

    user_id = Column(Integer, ForeignKey("users.id"))
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Relationships
    messages = relationship("Message", back_populates="chat")
    user = relationship("User", back_populates="chats")

    # Chat
    vector_db = VectorDatabase()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversational_chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.5, model="gpt-4"),
        vector_db.database.as_retriever(),
        memory=memory,
    )

    def get_messages(self) -> list[Message]:
        print(
            f"""\n{'_'*80}\nGetting the messages from the database for conversation id: {self.id}...\n\n{'_'*80}"""
        )

        messages: list[Message] = Message.query.filter_by(chat_id=self.id).all()
        for message in messages:
            print(message.content)

        return messages

    @classmethod
    def create_new_chat(cls, user_id: int) -> int:
        print(
            f"""\n{'_'*80}\nCreating new conversation in the database...\n\n{'_'*80}"""
        )
        new_chat = cls(user_id=user_id)  # type: ignore
        database.session.add(new_chat)
        database.session.commit()
        return new_chat.id  # type: ignore

    @classmethod
    def get_chat_by_id(cls, chat_id) -> "Chat":
        print(
            f"""\n{'_'*80}\nGetting conversation with id: {chat_id} from the database...\n\n{'_'*80}"""
        )
        return cls.query.filter_by(id=chat_id).first()  # type: ignore

    @classmethod
    def delete_chat_by_id(cls, chat_id: int) -> bool:
        print(
            f"\n{'_'*80}\nDeleting conversation with id: {chat_id} from the database...\n{'_'*80}"
        )

        # Fetch the chat to delete
        chat_to_delete = cls.query.filter_by(id=chat_id).first()

        if not chat_to_delete:
            print(f"No chat found with id: {chat_id}")
            return False

        # Deleting associated messages first
        Message.query.filter_by(chat_id=chat_id).delete()

        # Deleting the chat itself
        database.session.delete(chat_to_delete)

        # Committing the transaction
        database.session.commit()

        print(f"Successfully deleted chat with id: {chat_id}")
        return True

    @staticmethod
    def generate_ai_response(chat_id: int, user_query: str) -> str | None:
        if user_query.strip() == "":
            flash("Message cannot be empty.", "message_error")
            return

        print(f"\n{'_'*80}\nReceived user query: {user_query}\n{'_'*80}\n")

        # Add user message to DB
        Chat.add_chat_message(chat_id, user_query, "user_message")
        # Generate AI response
        result: dict = Chat.conversational_chain({"question": user_query})
        answer: str = result["answer"]
        print(f"\n{'_'*80}\nGenerated AI answer: {answer}\n{'_'*80}\n")
        # Add AI response to DB
        Chat.add_chat_message(chat_id, answer, "ai_message")

        return answer

    @staticmethod
    def add_chat_message(chat_id: int, content: str, message_type: str) -> None:
        Message.add_message(chat_id, content, message_type)

    @classmethod
    def update_chat_name_by_id(cls, chat_id: int, new_name: str) -> bool:
        """
        Update the chat name by its ID.

        This class method updates the chat name in the database.
        It uses Pydantic for input validation to ensure that the name is neither empty nor consists only of whitespace.

        Args:
            chat_id (int): The ID of the chat to update.
            new_name (str): The new name for the chat.

        Returns:
            bool: True if the update was successful, False otherwise.
        """

        try:
            # Validate the name using Pydantic
            validated_data = ChatSchema(name=new_name)
            new_name = validated_data.name

            # Fetch the chat by ID and update the name
            chat_to_update = cls.query.filter_by(id=chat_id).first()
            if not chat_to_update:
                flash(f"No chat found with id: {chat_id}", "chat_error")
                return False

            chat_to_update.name = new_name
            database.session.commit()
            return True

        except ValidationError as e:
            flash(f"Validation Error: {e}", "validation_error")
            return False

        except SQLAlchemyError as e:
            database.session.rollback()
            flash(f"An error occurred while updating the chat name: {e}", "db_error")
            return False


class ChatSchema(BaseModel):
    """
    Pydantic schema for Chat model.

    This class serves as the Pydantic schema for the Chat model.
    It's useful for data validation and serialization when working with APIs.
    Pydantic's BaseModel is subclassed to create the schema.
    Each attribute is strongly typed to ensure data integrity.

    Attributes:
        name (str): The name of the chat.

    Notes:
        Only validates the `name` attribute.  Exists for extensibility purposes.
    """

    name: str

    @validator("name", pre=True, always=True)
    def validate_name(cls, name):
        name = name.strip()
        if not name:
            raise ValueError("Chat name cannot be empty or whitespace.")
        return name


# # TODO: Use schema for validation
# class ChatSchema(BaseModel):
#     """
#     Pydantic schema for Chat model.

#     This class serves as the Pydantic schema for the Chat model.
#     It's useful for data validation and serialization when working with APIs.
#     Pydantic's BaseModel is subclassed to create the schema.
#     Each attribute is strongly typed to ensure data integrity.

#     Attributes:
#         id (int): Unique identifier for each chat.
#         created_at (datetime): The time the chat was created.
#         updated_at (datetime): The time the chat was last updated.
#         session_id (str): A string representing the session ID.
#     """

#     id: int
#     name: str
#     created_at: datetime
#     updated_at: datetime
#     session_id: str

from datetime import datetime
from pydantic import BaseModel
from flask_app import database
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Message(database.Model):
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


class MessageSchema(BaseModel):
    id: int
    content: str
    message_type: str
    created_at: datetime
    chat_id: int

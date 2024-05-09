from sqlalchemy import Integer, DateTime, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Self
from .entity_base import EntityBase
from models import ChatLogEntry
from datetime import datetime

class ChatEntity(EntityBase):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, unique=False)
    content: Mapped[str] = mapped_column(String, unique=False, index=True)
    author_id: Mapped[int] = mapped_column(BigInteger, unique=False, index=True)
    author_name: Mapped[str] = mapped_column(String(32), unique=False, index=True)

    @classmethod
    def from_model(cls, model: ChatLogEntry) -> Self:
        return cls(
            id=model['id'],
            timestamp=model['timestamp'],
            content=model['content'],
            author_id=model['author_id'],
            author_name=model['author_name']
        )

    def to_model(self) -> ChatLogEntry:
        return ChatLogEntry(
            id=self.id,
            timestamp=self.timestamp,
            content=self.content,
            author_id=self.author_id,
            author_name=self.author_name,
        )
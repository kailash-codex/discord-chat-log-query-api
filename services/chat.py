from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session

from entities.chat_entity import ChatEntity
from models.chatLogEntry import ChatLogEntry
from database import db_session

class ChatService:
    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def loadChatLog(self, chatEntry: ChatLogEntry) -> ChatLogEntry:
        """Load chat log entry into db table

        Args:
            chatEntry (ChatLogEntry): A single discord chat log entry

        Returns:
            chatEntry (ChatLogEntry): The chat entry made
        
        """
        existing_entry = self._session.query(ChatEntity).filter_by(id=chatEntry['id']).first()
        if existing_entry: return existing_entry.to_model()

        chat_log_entity = ChatEntity.from_model(chatEntry)
        self._session.add(chat_log_entity)
        self._session.commit()
        return chat_log_entity.to_model()
    
    def getEntriesBetweenDates(self, startDate: datetime, endDate: datetime) -> list:
        """Retrieve chat log entries within a specific date range.

        Args:
            start_date (datetime): The start of the date range.
            end_date (datetime): The end of the date range.

        Returns:
            list: A list of ChatLogEntry models.
        """
        # Query the database for entries within the date range
        entries = self._session.query(ChatEntity).filter(ChatEntity.timestamp >= startDate, ChatEntity.timestamp <= endDate).all()
        return [entry.to_model() for entry in entries]
    
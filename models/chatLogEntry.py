"""ChatLogEntry model serves as the data object for representing chat logs made in a certain channel."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatLogEntry(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    content: str = ""
    author_id: Optional[int] = None
    author_name: str = ""

    #for python v 3.11
    
    # id: int | None = None
    # timestamp: datetime | None = None
    # content: str = ""
    # author_id: int | None = None
    # author_name: str = ""
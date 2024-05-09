""" 
    API collection for handling chat queries
"""

from datetime import datetime
from models.exportrequest import ExportRequest
from api.utils.utils import exportChatsFromCli, reformatMessageLogs
from fastapi import APIRouter, Depends, HTTPException
from services.chat import ChatService

api = APIRouter(prefix="/chats")

@api.get("/")
def healthCheck():
    return {"status": "/chats endpoint is OK - 200"}


@api.post("/export")
def export_chat(data: ExportRequest, chatService: ChatService = Depends()):
    responseData = exportChatsFromCli(data)
    reformattedMessages = reformatMessageLogs(responseData['data']['messages'])
    try:
        for message in reformattedMessages:
            chatService.loadChatLog(message)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    return {"result": "Exported following chat messages to database", "messages": reformattedMessages}

@api.get("/range")
def get_chats_within_range(startDate: datetime, endDate: datetime, chatService: ChatService = Depends()):
    try:
        result = chatService.getEntriesBetweenDates(startDate, endDate)
        if not result: return {"result" : "No chat logs were found in given range"}
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    
@api.get("/search")
def search_content_for_substring_match(substring: str, chatService: ChatService = Depends()):
    try:
        result =  chatService.searchContent(substring)
        if not result: return {"result" : "No chat logs were found in given range"}
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
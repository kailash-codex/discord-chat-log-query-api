""" 
    API collection for handling chat queries
"""

from datetime import datetime
from models.exportrequest import ExportRequest
from api.utils.utils import exportChatsFromCli, reformatMessageLogs
from fastapi import APIRouter, Depends, HTTPException
import requests
from requests.exceptions import HTTPError
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
    return reformattedMessages

@api.get("/range")
def getChatsWithinRange(startDate: datetime, endDate: datetime, chatService: ChatService = Depends()):
    try:
        return chatService.getEntriesBetweenDates(startDate, endDate)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    


""" 
    API collection for handling chat queries
"""

from models.exportrequest import ExportRequest
from api.utils.utils import exportChatsFromCli
from fastapi import APIRouter

api = APIRouter(prefix="/chats")

@api.get("/")
def healthCheck():
    return {"status": "/chats endpoint is OK - 200"}


@api.post("/export")
def export_chat(data: ExportRequest):

    responseData = exportChatsFromCli(data)
    return responseData
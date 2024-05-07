""" 
    API collection for handling chat queries
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
import json
api = APIRouter(prefix="/chats")

from pydantic import BaseModel
import subprocess


class ExportRequest(BaseModel):
    token: str
    channel_id: str
    format: str = "json"


@api.get("/")
def healthCheck():
    return {"status": "/chats endpoint is OK - 200"}


@api.post("/export")
def export_chat(data: ExportRequest):
    sevenDaysPrior = datetime.now() - timedelta(hours=1)
    # sevenDaysPrior = datetime.now() - timedelta(days=1, hours=-3)

    sevenDaysPrior = sevenDaysPrior.strftime("%Y-%m-%d, %H:%M:%S")

    command = f"dotnet DiscordChatExporter.Cli/DiscordChatExporter.Cli.dll export -t {data.token} -c {data.channel_id} -f {data.format} --after '{sevenDaysPrior}' -o exportResponse.json"

    response = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    dataOutput = None
    try:
        with open('exportResponse.json', 'r') as file:
            dataOutput = json.load(file)
        print("JSON loaded successfully.")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")

    if response.returncode == 0 and dataOutput:
        return {"status": "success", "data": dataOutput}
    else:
        raise HTTPException(status_code=400, detail=response.stderr)

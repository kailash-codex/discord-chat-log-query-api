from datetime import datetime, timedelta
from fastapi import HTTPException
import json
import subprocess

from models.exportrequest import ExportRequest

def exportChatsFromCli(data: ExportRequest):
    sevenDaysPrior = datetime.now() - timedelta(hours=1)
    # sevenDaysPrior = datetime.now() - timedelta(days=1, hours=3)

    sevenDaysPrior = sevenDaysPrior.strftime("%Y-%m-%d, %H:%M:%S")

    command = f"dotnet DiscordChatExporter.Cli/DiscordChatExporter.Cli.dll export -t {data.token} -c {data.channel_id} -f Json --after '{sevenDaysPrior}' -o exportResponse.json"

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

from datetime import datetime, timedelta
from fastapi import HTTPException
import json
import subprocess

from models.exportrequest import ExportRequest

def exportChatsFromCli(data: ExportRequest):
    sevenDaysPrior = datetime.now() - timedelta(days=7)
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


def reformatMessageLogs(messageList):
    return [reformatLog(message) for message in messageList]
    

def reformatLog(message):
    reformattedMessage = {}

    reformattedMessage['id'] = int(message.get('id', None))
    
    reformattedMessage['timestamp'] = datetime.fromisoformat(adjust_iso_format(message.get('timestamp', None)))
    reformattedMessage['content'] = message.get('content', None)

    if 'author' in message:
        if 'id' in message['author']:
            reformattedMessage['author_id'] = int(message['author']['id'])
        
        if 'name' in message['author']:
            reformattedMessage['author_name'] = message['author']['name']

    return reformattedMessage


"""
Rare cases where the Discord Chat Export cli application doesn't properly send the timestamp in ISO format
Ex: 2024-05-08T21:10:19.4-04:00
"""
def adjust_iso_format(date_str):
    parts = date_str.split('.')
    if len(parts) == 2:
        sec_fraction, tz = parts[1].split('-')
        sec_fraction = sec_fraction.ljust(3, '0')  # Pad the fractional part to three digits
        adjusted_date_str = f'{parts[0]}.{sec_fraction}-{tz}'
    else:
        adjusted_date_str = date_str
    return adjusted_date_str
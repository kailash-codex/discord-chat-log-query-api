from pydantic import BaseModel

class ExportRequest(BaseModel):
    channel_id: str
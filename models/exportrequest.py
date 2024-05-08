from pydantic import BaseModel

class ExportRequest(BaseModel):
    token: str
    channel_id: str
from typing import Optional
from pydantic import BaseModel

class SendMessageSchema(BaseModel):
    body: str
    to: str

class MessageReceivedSchema(BaseModel):
    profile_name: str
    message_from: str
    body: str
    message_id: str

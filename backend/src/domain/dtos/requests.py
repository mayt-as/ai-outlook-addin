from pydantic import BaseModel
from typing import Optional, List

class SummaryRequest(BaseModel):
    message_id: str
    summary_type: str = "concise" # concise, detailed, executive

class ThreadSummaryRequest(BaseModel):
    conversation_id: str

class ReplyRequest(BaseModel):
    message_id: str
    instructions: str
    tone: Optional[str] = "professional"

class DraftRequest(BaseModel):
    instructions: str
    tone: Optional[str] = "professional"
    
class RewriteRequest(BaseModel):
    selected_text: str
    tone: str = "professional"

class ActionItemsRequest(BaseModel):
    message_id: str

class PriorityRequest(BaseModel):
    message_id: str

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SummaryResponse(BaseModel):
    summary: str

class ActionItem(BaseModel):
    task: str
    owner: Optional[str]
    deadline: Optional[str]
    risk: Optional[str]

class ActionItemsResponse(BaseModel):
    items: List[ActionItem]

class PriorityResponse(BaseModel):
    priority: str # Low, Medium, High, Urgent
    reason: str

class GeneratedTextResponse(BaseModel):
    text: str

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IAIProvider(ABC):
    @abstractmethod
    async def generate_text(self, system_prompt: str, user_prompt: str, max_tokens: int = 1000) -> str:
        pass
    
    @abstractmethod
    async def generate_structured_data(self, system_prompt: str, user_prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        pass

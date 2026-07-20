import structlog
from typing import Dict, Any, List
from services.ai.openai_compatible_provider import OpenAICompatibleProvider
from prompts.prompt_manager import prompt_manager
from domain.dtos.responses import ActionItemsResponse, PriorityResponse

logger = structlog.get_logger(__name__)

class BusinessAIService:
    def __init__(self):
        self.ai = OpenAICompatibleProvider()

    async def generate_summary(self, email_content: str, summary_type: str = "concise") -> str:
        prompt = prompt_manager.get_prompt("summary")
        sys_prompt = prompt.system_prompt + f"\n\nCreate a {summary_type} summary."
        user_prompt = prompt.user_prompt.format(email_content=email_content)
        return await self.ai.generate_text(sys_prompt, user_prompt)

    async def generate_draft(self, instructions: str, tone: str) -> str:
        sys_prompt = f"You are an expert email copywriter. Write an email in a {tone} tone based on the instructions."
        user_prompt = f"Instructions:\n{instructions}"
        return await self.ai.generate_text(sys_prompt, user_prompt)

    async def rewrite_text(self, text: str, tone: str) -> str:
        sys_prompt = f"You are an expert editor. Rewrite the provided text to be {tone}."
        user_prompt = f"Text to rewrite:\n{text}"
        return await self.ai.generate_text(sys_prompt, user_prompt)

    async def extract_action_items(self, email_content: str) -> dict:
        sys_prompt = "Extract all action items, tasks, owners, deadlines, and risks from the email."
        user_prompt = email_content
        schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string"},
                            "owner": {"type": "string", "nullable": True},
                            "deadline": {"type": "string", "nullable": True},
                            "risk": {"type": "string", "nullable": True}
                        },
                        "required": ["task"]
                    }
                }
            },
            "required": ["items"]
        }
        return await self.ai.generate_structured_data(sys_prompt, user_prompt, schema)

    async def classify_priority(self, email_content: str) -> dict:
        sys_prompt = "Classify the priority of the following email into: Low, Medium, High, or Urgent. Also provide a brief reason."
        user_prompt = email_content
        schema = {
            "type": "object",
            "properties": {
                "priority": {"type": "string", "enum": ["Low", "Medium", "High", "Urgent"]},
                "reason": {"type": "string"}
            },
            "required": ["priority", "reason"]
        }
        return await self.ai.generate_structured_data(sys_prompt, user_prompt, schema)

business_ai_service = BusinessAIService()

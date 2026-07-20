import httpx
import structlog
import json
from typing import Dict, Any
from core.config import get_settings
from core.exceptions import AIProviderException
from services.ai.provider_interface import IAIProvider
import asyncio

logger = structlog.get_logger(__name__)

class OpenAICompatibleProvider(IAIProvider):
    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _call_api(self, api_base: str, api_key: str, model: str, messages: list, retries: int = 2) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.2
        }
        
        for attempt in range(retries):
            try:
                response = await self.client.post(f"{api_base.rstrip('/')}/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error("AI API HTTP Error", status_code=e.response.status_code, response=e.response.text)
                if e.response.status_code >= 500:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise AIProviderException(f"AI API Error: {e.response.status_code}")
            except httpx.RequestError as e:
                logger.error("AI API Request Error", error=str(e))
                await asyncio.sleep(2 ** attempt)
                continue
        raise AIProviderException("Failed to communicate with AI provider after retries")

    async def _execute_with_fallback(self, messages: list) -> Dict[str, Any]:
        try:
            logger.info("Calling primary AI model", model=self.settings.primary_model)
            return await self._call_api(
                self.settings.openai_api_base, 
                self.settings.openai_api_key, 
                self.settings.primary_model, 
                messages
            )
        except AIProviderException as e:
            logger.warn("Primary AI failed, attempting fallback", error=str(e))
            if self.settings.fallback_api_base and self.settings.fallback_api_key:
                return await self._call_api(
                    self.settings.fallback_api_base,
                    self.settings.fallback_api_key,
                    self.settings.fallback_model,
                    messages
                )
            raise e

    async def generate_text(self, system_prompt: str, user_prompt: str, max_tokens: int = 1000) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        result = await self._execute_with_fallback(messages)
        return result["choices"][0]["message"]["content"]

    async def generate_structured_data(self, system_prompt: str, user_prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        # Append schema instructions to system prompt to enforce JSON output
        schema_instruction = f"\n\nYou MUST return ONLY valid JSON matching this schema: {json.dumps(schema)}"
        messages = [
            {"role": "system", "content": system_prompt + schema_instruction},
            {"role": "user", "content": user_prompt}
        ]
        result = await self._execute_with_fallback(messages)
        content = result["choices"][0]["message"]["content"]
        
        # Strip markdown formatting if the model wrapped it in ```json
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        try:
            return json.loads(content.strip())
        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI JSON response", response=content, error=str(e))
            raise AIProviderException("AI model returned invalid JSON structure")

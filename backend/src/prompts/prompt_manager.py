import os
import yaml
from typing import Dict, Any, Optional
from pydantic import BaseModel
import structlog

logger = structlog.get_logger(__name__)

class PromptConfig(BaseModel):
    name: str
    version: str
    system_prompt: str
    user_prompt: str

class PromptManager:
    def __init__(self, prompts_dir: str = "src/prompts/definitions"):
        self.prompts_dir = prompts_dir
        self.prompts: Dict[str, PromptConfig] = {}
        self._load_prompts()

    def _load_prompts(self):
        if not os.path.exists(self.prompts_dir):
            os.makedirs(self.prompts_dir, exist_ok=True)
            logger.info("Created prompts directory", path=self.prompts_dir)
            return

        for filename in os.listdir(self.prompts_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(self.prompts_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            prompt_config = PromptConfig(**data)
                            key = f"{prompt_config.name}_v{prompt_config.version}"
                            self.prompts[key] = prompt_config
                            # Also store the latest version by name
                            self.prompts[prompt_config.name] = prompt_config
                except Exception as e:
                    logger.error("Failed to load prompt file", file=filename, error=str(e))

    def get_prompt(self, name: str, version: Optional[str] = None) -> PromptConfig:
        key = f"{name}_v{version}" if version else name
        prompt = self.prompts.get(key)
        if not prompt:
            raise ValueError(f"Prompt '{key}' not found.")
        return prompt

prompt_manager = PromptManager()

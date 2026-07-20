import pytest
from unittest.mock import patch, AsyncMock
from prompts.prompt_manager import PromptManager
from services.ai.openai_compatible_provider import OpenAICompatibleProvider
from core.exceptions import AIProviderException
import os

def test_prompt_manager_loads_prompts(tmp_path):
    # Setup mock prompt directory
    import yaml
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    prompt_file = prompts_dir / "test_prompt.yaml"
    
    test_data = {
        "name": "test",
        "version": "1.0",
        "system_prompt": "sys prompt",
        "user_prompt": "user prompt {var}"
    }
    with open(prompt_file, 'w') as f:
        yaml.dump(test_data, f)
        
    pm = PromptManager(prompts_dir=str(prompts_dir))
    prompt = pm.get_prompt("test")
    assert prompt.name == "test"
    assert prompt.version == "1.0"
    
@pytest.mark.asyncio
async def test_ai_provider_fallback():
    provider = OpenAICompatibleProvider()
    
    # Mock _call_api to fail on first call and succeed on second (fallback)
    provider._call_api = AsyncMock(side_effect=[
        AIProviderException("Primary failed"),
        {"choices": [{"message": {"content": "fallback success"}}]}
    ])
    
    result = await provider.generate_text("sys", "user")
    assert result == "fallback success"
    assert provider._call_api.call_count == 2

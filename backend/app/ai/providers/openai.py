import json

from openai import AsyncOpenAI

from app.ai.contracts import ModelRequest, ModelResponse
from app.core.config import get_settings
from app.core.errors import DomainError


class OpenAIProvider:
    """OpenAI Responses API adapter with structured-output support."""

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            raise DomainError("ai_not_configured", "AI service is not configured", 503)
        self.model = settings.openai_model
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self, request: ModelRequest) -> ModelResponse:
        text_config: dict[str, object] = {}
        if request.response_schema:
            text_config["format"] = {
                "type": "json_schema",
                "name": "namo_agent_response",
                "strict": True,
                "schema": request.response_schema,
            }
        response = await self.client.responses.create(
            model=self.model,
            instructions=request.system_prompt,
            input=request.user_prompt,
            text=text_config,
            max_output_tokens=request.max_output_tokens,
            store=False,
        )
        output = response.output_text
        if request.response_schema:
            json.loads(output)
        usage = response.usage
        return ModelResponse(
            text=output,
            model=self.model,
            input_tokens=usage.input_tokens if usage else 0,
            output_tokens=usage.output_tokens if usage else 0,
        )

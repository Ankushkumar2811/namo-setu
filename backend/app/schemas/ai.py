from uuid import UUID

from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    conversation_id: UUID | None = None
    message: str = Field(min_length=2, max_length=4_000)
    language: str = Field(default="en-IN", min_length=2, max_length=12)


class SourceResponse(BaseModel):
    title: str
    url: str | None


class AIChatResponse(BaseModel):
    conversation_id: UUID
    answer: str
    confidence: float = Field(ge=0, le=1)
    agents: list[str]
    sources: list[SourceResponse]
    suggestions: list[str]
    actions_executed: list[str] = []

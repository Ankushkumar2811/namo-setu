from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Citation:
    source_id: str
    title: str
    url: str | None
    excerpt: str
    retrieved_at: str


@dataclass(frozen=True)
class AgentContext:
    user_id: str
    conversation_id: str
    language: str
    query: str
    memories: dict[str, str] = field(default_factory=dict)
    evidence: tuple[Citation, ...] = ()


@dataclass(frozen=True)
class AgentResult:
    agent: str
    content: str
    confidence: float
    citations: tuple[Citation, ...] = ()
    warnings: tuple[str, ...] = ()
    proposed_actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ModelRequest:
    system_prompt: str
    user_prompt: str
    response_schema: dict[str, object] | None = None
    max_output_tokens: int = 1800


@dataclass(frozen=True)
class ModelResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int


class ModelProvider(Protocol):
    async def generate(self, request: ModelRequest) -> ModelResponse: ...


class KnowledgeRetriever(Protocol):
    async def search(self, query: str, filters: dict[str, str], limit: int = 8) -> tuple[Citation, ...]: ...

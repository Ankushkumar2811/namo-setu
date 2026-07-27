import asyncio
import json

from app.ai.agents import SpecialistAgent
from app.ai.contracts import AgentContext, AgentResult, KnowledgeRetriever, ModelProvider, ModelRequest
from app.ai.prompts import SYNTHESIS_PROMPT
from app.ai.routing import IntentRouter
from app.ai.safety import SafetyGuard
from app.core.config import get_settings
from app.core.errors import DomainError

SYNTHESIS_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "follow_up_suggestions": {"type": "array", "items": {"type": "string"}, "maxItems": 4},
    },
    "required": ["answer", "confidence", "follow_up_suggestions"],
    "additionalProperties": False,
}


class NamoOrchestrator:
    """Route, retrieve, fan out to specialists and synthesize one evidence-grounded answer."""

    def __init__(self, provider: ModelProvider, retriever: KnowledgeRetriever) -> None:
        self.provider = provider
        self.retriever = retriever
        self.router = IntentRouter()
        self.guard = SafetyGuard()
        self.settings = get_settings()

    async def execute(self, context: AgentContext) -> tuple[str, float, tuple[AgentResult, ...], list[str]]:
        decision = self.guard.inspect_input(context.query)
        if not decision.allowed:
            raise DomainError("unsafe_prompt", "This request cannot be processed safely", 400)
        evidence = await self.retriever.search(context.query, {}, limit=8)
        enriched = AgentContext(
            user_id=context.user_id,
            conversation_id=context.conversation_id,
            language=context.language,
            query=context.query,
            memories=context.memories,
            evidence=evidence,
        )
        agent_names = self.router.route(context.query, self.settings.ai_max_parallel_agents)
        results = tuple(
            await asyncio.gather(*(SpecialistAgent(name, self.provider).run(enriched) for name in agent_names))
        )
        reports = "\n\n".join(
            f"## {result.agent}\n{result.content}\nConfidence: {result.confidence}\n"
            f"Warnings: {list(result.warnings)}\nProposed only: {list(result.proposed_actions)}"
            for result in results
        )
        synthesis = await self.provider.generate(
            ModelRequest(
                system_prompt=SYNTHESIS_PROMPT,
                user_prompt=f"User request: {context.query}\nSpecialist reports:\n{reports}",
                response_schema=SYNTHESIS_SCHEMA,
                max_output_tokens=2400,
            )
        )
        payload = json.loads(synthesis.text)
        confidence = min(float(payload["confidence"]), *(result.confidence for result in results))
        if decision.risk == "emergency":
            confidence = min(confidence, 0.7)
        return payload["answer"], confidence, results, payload["follow_up_suggestions"]

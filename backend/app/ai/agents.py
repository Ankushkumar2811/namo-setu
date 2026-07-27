import json

from app.ai.contracts import AgentContext, AgentResult, ModelProvider, ModelRequest
from app.ai.prompts import AGENT_PROMPTS

AGENT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "warnings": {"type": "array", "items": {"type": "string"}},
        "proposed_actions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["answer", "confidence", "warnings", "proposed_actions"],
    "additionalProperties": False,
}


class SpecialistAgent:
    def __init__(self, name: str, provider: ModelProvider) -> None:
        if name not in AGENT_PROMPTS:
            raise ValueError(f"Unknown agent: {name}")
        self.name = name
        self.provider = provider

    async def run(self, context: AgentContext) -> AgentResult:
        evidence = "\n".join(
            f"[{index + 1}] {item.title}: {item.excerpt}" for index, item in enumerate(context.evidence)
        ) or "No authoritative evidence was retrieved. State uncertainty."
        prompt = (
            f"User query: {context.query}\nLanguage: {context.language}\n"
            f"Consented preferences: {context.memories}\nEvidence:\n{evidence}"
        )
        response = await self.provider.generate(
            ModelRequest(
                system_prompt=AGENT_PROMPTS[self.name],
                user_prompt=prompt,
                response_schema=AGENT_SCHEMA,
            )
        )
        payload = json.loads(response.text)
        return AgentResult(
            agent=self.name,
            content=payload["answer"],
            confidence=float(payload["confidence"]),
            citations=context.evidence,
            warnings=tuple(payload["warnings"]),
            proposed_actions=tuple(payload["proposed_actions"]),
        )

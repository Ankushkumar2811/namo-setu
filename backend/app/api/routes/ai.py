import json
import time

from fastapi import APIRouter
from sqlalchemy import select

from app.ai.contracts import AgentContext
from app.ai.orchestrator import NamoOrchestrator
from app.ai.providers.openai import OpenAIProvider
from app.ai.rag import PostgresKnowledgeRetriever
from app.api.dependencies import CurrentUser, Session
from app.core.errors import DomainError
from app.models.entities import AIConversation, AIMessage
from app.schemas.ai import AIChatRequest, AIChatResponse, SourceResponse

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat", response_model=AIChatResponse)
async def chat(payload: AIChatRequest, user: CurrentUser, session: Session) -> AIChatResponse:
    if payload.conversation_id:
        conversation = await session.scalar(
            select(AIConversation).where(
                AIConversation.id == payload.conversation_id,
                AIConversation.user_id == user.id,
                AIConversation.deleted_at.is_(None),
            )
        )
        if conversation is None:
            raise DomainError("conversation_not_found", "Conversation was not found", 404)
    else:
        conversation = AIConversation(
            user_id=user.id,
            title=payload.message[:120],
            language=payload.language,
        )
        session.add(conversation)
        await session.flush()
    session.add(AIMessage(conversation_id=conversation.id, role="user", content=payload.message))
    started = time.perf_counter()
    orchestrator = NamoOrchestrator(OpenAIProvider(), PostgresKnowledgeRetriever(session))
    answer, confidence, results, suggestions = await orchestrator.execute(
        AgentContext(
            user_id=str(user.id),
            conversation_id=str(conversation.id),
            language=payload.language,
            query=payload.message,
        )
    )
    citations = {item.source_id: item for result in results for item in result.citations}
    session.add(
        AIMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
            citations_json=json.dumps([item.__dict__ for item in citations.values()]),
            confidence=confidence,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )
    )
    return AIChatResponse(
        conversation_id=conversation.id,
        answer=answer,
        confidence=confidence,
        agents=[result.agent for result in results],
        sources=[SourceResponse(title=item.title, url=item.url) for item in citations.values()],
        suggestions=suggestions,
    )

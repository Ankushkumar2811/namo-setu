from datetime import UTC, datetime

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.contracts import Citation
from app.ai.safety import SafetyGuard
from app.models.entities import Temple


class PostgresKnowledgeRetriever:
    """Authoritative lexical retrieval; vector search can be composed behind the same contract."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.guard = SafetyGuard()

    async def search(self, query: str, filters: dict[str, str], limit: int = 8) -> tuple[Citation, ...]:
        pattern = f"%{query[:120]}%"
        statement = select(Temple).where(
            Temple.deleted_at.is_(None),
            or_(Temple.name.ilike(pattern), Temple.description.ilike(pattern), Temple.city.ilike(pattern)),
        )
        if state := filters.get("state"):
            statement = statement.where(Temple.state == state)
        temples = (await self.session.scalars(statement.limit(limit))).all()
        return tuple(
            Citation(
                source_id=str(temple.id),
                title=temple.name,
                url=f"/temples/{temple.slug}",
                excerpt=self.guard.sanitize_evidence(temple.description),
                retrieved_at=datetime.now(UTC).isoformat(),
            )
            for temple in temples
        )

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import Temple, TempleCrowd


class TempleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, query: str | None, state: str | None, offset: int, limit: int) -> tuple[list[Temple], int]:
        statement = select(Temple).where(Temple.deleted_at.is_(None))
        count_statement = select(func.count(Temple.id)).where(Temple.deleted_at.is_(None))
        if query:
            predicate = Temple.name.ilike(f"%{query}%")
            statement = statement.where(predicate)
            count_statement = count_statement.where(predicate)
        if state:
            statement = statement.where(Temple.state == state)
            count_statement = count_statement.where(Temple.state == state)
        statement = statement.order_by(Temple.rating.desc(), Temple.name).offset(offset).limit(limit)
        return list((await self.session.scalars(statement)).all()), int(await self.session.scalar(count_statement) or 0)

    async def by_id(self, temple_id: UUID) -> Temple | None:
        return await self.session.scalar(
            select(Temple).where(Temple.id == temple_id, Temple.deleted_at.is_(None))
        )

    async def latest_crowd(self, temple_id: UUID) -> TempleCrowd | None:
        return await self.session.scalar(
            select(TempleCrowd)
            .where(TempleCrowd.temple_id == temple_id, TempleCrowd.deleted_at.is_(None))
            .order_by(TempleCrowd.observed_at.desc())
            .limit(1)
        )

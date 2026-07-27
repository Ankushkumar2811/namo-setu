from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.errors import DomainError
from app.core.security import decode_access_token
from app.models.entities import User

Session = Annotated[AsyncSession, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session) -> User:
    user_id: UUID = decode_access_token(token)
    user = await session.scalar(
        select(User).where(User.id == user_id, User.is_active.is_(True), User.deleted_at.is_(None))
    )
    if user is None:
        raise DomainError("user_not_found", "Authenticated user no longer exists", 401)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

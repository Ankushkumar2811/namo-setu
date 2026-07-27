import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, status
from sqlalchemy import select

from app.api.dependencies import Session
from app.core.config import get_settings
from app.core.errors import DomainError
from app.core.security import create_token, hash_password, verify_password
from app.models.entities import RefreshToken, User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
settings = get_settings()


def issue_tokens(user: User) -> tuple[TokenResponse, RefreshToken]:
    refresh_value = create_token(user.id, "refresh", timedelta(days=settings.refresh_token_days))
    response = TokenResponse(
        access_token=create_token(user.id, "access", timedelta(minutes=settings.access_token_minutes)),
        refresh_token=refresh_value,
        expires_in=settings.access_token_minutes * 60,
    )
    record = RefreshToken(
        user_id=user.id,
        token_hash=hashlib.sha256(refresh_value.encode()).hexdigest(),
        expires_at=datetime.now(UTC) + timedelta(days=settings.refresh_token_days),
    )
    return response, record


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, session: Session) -> TokenResponse:
    existing = await session.scalar(select(User.id).where(User.email == payload.email.lower()))
    if existing:
        raise DomainError("email_registered", "An account already uses this email", 409)
    user = User(
        email=payload.email.lower(),
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
    )
    session.add(user)
    await session.flush()
    response, refresh = issue_tokens(user)
    session.add(refresh)
    return response


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: Session) -> TokenResponse:
    user = await session.scalar(
        select(User).where(User.email == payload.email.lower(), User.deleted_at.is_(None))
    )
    if user is None or not verify_password(payload.password, user.password_hash):
        secrets.compare_digest("constant-time-padding", "invalid-credential")
        raise DomainError("invalid_credentials", "Email or password is incorrect", 401)
    if not user.is_active:
        raise DomainError("account_disabled", "This account is disabled", 403)
    response, refresh = issue_tokens(user)
    session.add(refresh)
    return response

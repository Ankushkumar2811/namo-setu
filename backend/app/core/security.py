from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash

from app.core.config import get_settings

password_hash = PasswordHash.recommended()
settings = get_settings()


def hash_password(password: str) -> str:
    """Hash a password with Argon2id."""
    return password_hash.hash(password)


def verify_password(password: str, encoded: str) -> bool:
    """Compare a supplied password with an Argon2id hash."""
    return password_hash.verify(password, encoded)


def create_token(subject: UUID, token_type: str, expires: timedelta) -> str:
    """Create a signed JWT with issuer, type and expiration claims."""
    now = datetime.now(UTC)
    claims = {
        "sub": str(subject),
        "type": token_type,
        "iss": settings.jwt_issuer,
        "iat": now,
        "exp": now + expires,
    }
    return jwt.encode(claims, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> UUID:
    """Validate an access token and return its user identifier."""
    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            issuer=settings.jwt_issuer,
        )
        if claims.get("type") != "access":
            raise ValueError("Incorrect token type")
        return UUID(claims["sub"])
    except (jwt.PyJWTError, ValueError, KeyError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "invalid_token", "message": "Authentication token is invalid or expired"},
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampedSoftDelete


class User(TimestampedSoftDelete, Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="user", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)


class Temple(TimestampedSoftDelete, Base):
    __tablename__ = "temples"
    __table_args__ = (
        Index("ix_temples_state_city", "state", "city"),
        CheckConstraint("rating >= 0 AND rating <= 5", name="rating_range"),
    )
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    deity: Mapped[str | None] = mapped_column(String(120), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    city: Mapped[str] = mapped_column(String(120), index=True)
    state: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(Text)
    latitude: Mapped[Decimal] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Decimal] = mapped_column(Numeric(9, 6))
    rating: Mapped[Decimal] = mapped_column(Numeric(2, 1), default=0)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, index=True)


class TempleCrowd(TimestampedSoftDelete, Base):
    __tablename__ = "temple_crowd"
    temple_id: Mapped[UUID] = mapped_column(ForeignKey("temples.id"), index=True)
    level: Mapped[str] = mapped_column(String(16), index=True)
    queue_minutes: Mapped[int]
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    source: Mapped[str] = mapped_column(String(40))


class Booking(TimestampedSoftDelete, Base):
    __tablename__ = "bookings"
    __table_args__ = (
        Index("ix_bookings_user_created", "user_id", "created_at"),
        CheckConstraint("amount_inr >= 0", name="amount_non_negative"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    reference: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    product_type: Mapped[str] = mapped_column(String(32), index=True)
    product_id: Mapped[UUID]
    status: Mapped[str] = mapped_column(String(32), default="pending_payment", index=True)
    service_date: Mapped[date] = mapped_column(Date, index=True)
    amount_inr: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    idempotency_key: Mapped[str] = mapped_column(String(80), unique=True)


class RefreshToken(TimestampedSoftDelete, Base):
    __tablename__ = "refresh_tokens"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuditLog(TimestampedSoftDelete, Base):
    __tablename__ = "audit_logs"
    actor_id: Mapped[UUID | None] = mapped_column(index=True)
    action: Mapped[str] = mapped_column(String(100), index=True)
    entity_type: Mapped[str] = mapped_column(String(80), index=True)
    entity_id: Mapped[UUID | None] = mapped_column(index=True)
    ip_address: Mapped[str | None] = mapped_column(String(45))
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")

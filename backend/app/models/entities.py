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


class AIConversation(TimestampedSoftDelete, Base):
    __tablename__ = "ai_conversations"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(160))
    language: Mapped[str] = mapped_column(String(12), default="en-IN", index=True)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)


class AIMessage(TimestampedSoftDelete, Base):
    __tablename__ = "ai_messages"
    __table_args__ = (Index("ix_ai_messages_conversation_created", "conversation_id", "created_at"),)
    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("ai_conversations.id"), index=True)
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    citations_json: Mapped[str] = mapped_column(Text, default="[]")
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(3, 2))
    model: Mapped[str | None] = mapped_column(String(80), index=True)
    latency_ms: Mapped[int | None]
    input_tokens: Mapped[int | None]
    output_tokens: Mapped[int | None]


class AIMemory(TimestampedSoftDelete, Base):
    __tablename__ = "ai_memories"
    __table_args__ = (
        Index("ix_ai_memories_user_category", "user_id", "category"),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="memory_confidence_range"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    category: Mapped[str] = mapped_column(String(40), index=True)
    key: Mapped[str] = mapped_column(String(100))
    encrypted_value: Mapped[str] = mapped_column(Text)
    confidence: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=1)
    consent_source: Mapped[str] = mapped_column(String(40))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)


class Organization(TimestampedSoftDelete, Base):
    __tablename__ = "organizations"
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    organization_type: Mapped[str] = mapped_column(String(40), index=True)
    state: Mapped[str | None] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    settings_json: Mapped[str] = mapped_column(Text, default="{}")


class Permission(TimestampedSoftDelete, Base):
    __tablename__ = "permissions"
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(240))
    module: Mapped[str] = mapped_column(String(60), index=True)


class OrganizationMember(TimestampedSoftDelete, Base):
    __tablename__ = "organization_members"
    __table_args__ = (
        Index("ix_org_members_org_user", "organization_id", "user_id", unique=True),
    )
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str] = mapped_column(String(40), index=True)
    permissions_json: Mapped[str] = mapped_column(Text, default="[]")
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)


class PartnerProfile(TimestampedSoftDelete, Base):
    __tablename__ = "partner_profiles"
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), unique=True)
    partner_type: Mapped[str] = mapped_column(String(40), index=True)
    legal_name: Mapped[str] = mapped_column(String(200))
    tax_identifier: Mapped[str | None] = mapped_column(String(40), index=True)
    verification_status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    commission_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    payout_status: Mapped[str] = mapped_column(String(20), default="on_hold", index=True)


class SupportTicket(TimestampedSoftDelete, Base):
    __tablename__ = "support_tickets"
    __table_args__ = (Index("ix_support_status_priority", "status", "priority"),)
    organization_id: Mapped[UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    reference: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    subject: Mapped[str] = mapped_column(String(240))
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    priority: Mapped[str] = mapped_column(String(16), default="normal", index=True)
    assigned_to: Mapped[UUID | None] = mapped_column(index=True)
    sla_due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class CRMLead(TimestampedSoftDelete, Base):
    __tablename__ = "crm_leads"
    organization_id: Mapped[UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    owner_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    full_name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str | None] = mapped_column(String(320), index=True)
    phone: Mapped[str | None] = mapped_column(String(20), index=True)
    stage: Mapped[str] = mapped_column(String(30), default="new", index=True)
    source: Mapped[str] = mapped_column(String(40), index=True)
    estimated_value_inr: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    next_action_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)


class FeatureFlag(TimestampedSoftDelete, Base):
    __tablename__ = "feature_flags"
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    rollout_percentage: Mapped[int] = mapped_column(default=0)
    organization_id: Mapped[UUID | None] = mapped_column(ForeignKey("organizations.id"), index=True)
    rules_json: Mapped[str] = mapped_column(Text, default="{}")

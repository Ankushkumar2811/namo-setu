import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select

from app.api.dependencies import Session, require_roles
from app.core.errors import DomainError
from app.models.entities import AuditLog, Booking, PartnerProfile, SupportTicket, User
from app.schemas.admin import (
    AdminDashboardResponse,
    DashboardMetric,
    PartnerResponse,
    PartnerReviewRequest,
)
from app.schemas.common import Page, PageMeta

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
    dependencies=[Depends(require_roles("super_admin", "regional_admin"))],
)


@router.get("/dashboard", response_model=AdminDashboardResponse)
async def dashboard(session: Session) -> AdminDashboardResponse:
    users = int(await session.scalar(select(func.count(User.id)).where(User.deleted_at.is_(None))) or 0)
    bookings = int(
        await session.scalar(select(func.count(Booking.id)).where(Booking.deleted_at.is_(None))) or 0
    )
    revenue = Decimal(
        await session.scalar(
            select(func.coalesce(func.sum(Booking.amount_inr), 0)).where(
                Booking.status.in_(("confirmed", "completed")), Booking.deleted_at.is_(None)
            )
        )
        or 0
    )
    open_tickets = int(
        await session.scalar(
            select(func.count(SupportTicket.id)).where(
                SupportTicket.status.in_(("open", "escalated")), SupportTicket.deleted_at.is_(None)
            )
        )
        or 0
    )
    pending_partners = int(
        await session.scalar(
            select(func.count(PartnerProfile.id)).where(
                PartnerProfile.verification_status == "pending",
                PartnerProfile.deleted_at.is_(None),
            )
        )
        or 0
    )
    return AdminDashboardResponse(
        generated_at=datetime.now(UTC),
        metrics=[
            DashboardMetric(key="users", label="Total users", value=users),
            DashboardMetric(key="bookings", label="Bookings", value=bookings),
            DashboardMetric(key="revenue", label="Gross revenue INR", value=revenue),
        ],
        open_support_tickets=open_tickets,
        pending_partner_verifications=pending_partners,
        active_alerts=0,
    )


@router.get("/partners", response_model=Page[PartnerResponse])
async def list_partners(
    session: Session,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[str | None, Query(max_length=20)] = None,
) -> Page[PartnerResponse]:
    statement = select(PartnerProfile).where(PartnerProfile.deleted_at.is_(None))
    count = select(func.count(PartnerProfile.id)).where(PartnerProfile.deleted_at.is_(None))
    if status:
        statement = statement.where(PartnerProfile.verification_status == status)
        count = count.where(PartnerProfile.verification_status == status)
    items = (
        await session.scalars(
            statement.order_by(PartnerProfile.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    ).all()
    return Page(
        items=[PartnerResponse.model_validate(item) for item in items],
        meta=PageMeta(page=page, page_size=page_size, total=int(await session.scalar(count) or 0)),
    )


@router.post("/partners/{partner_id}/review", response_model=PartnerResponse)
async def review_partner(
    partner_id: UUID,
    payload: PartnerReviewRequest,
    session: Session,
    admin=Depends(require_roles("super_admin", "regional_admin")),
) -> PartnerResponse:
    partner = await session.scalar(
        select(PartnerProfile).where(
            PartnerProfile.id == partner_id, PartnerProfile.deleted_at.is_(None)
        )
    )
    if partner is None:
        raise DomainError("partner_not_found", "Partner was not found", 404)
    partner.verification_status = {
        "approve": "verified",
        "reject": "rejected",
        "request_changes": "changes_requested",
    }[payload.decision]
    session.add(
        AuditLog(
            actor_id=admin.id,
            action=f"partner.{payload.decision}",
            entity_type="partner_profile",
            entity_id=partner.id,
            metadata_json=json.dumps({"note": payload.note}),
        )
    )
    await session.flush()
    return PartnerResponse.model_validate(partner)

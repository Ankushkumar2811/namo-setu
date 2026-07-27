from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DashboardMetric(BaseModel):
    key: str
    label: str
    value: Decimal
    change_percent: Decimal | None = None


class AdminDashboardResponse(BaseModel):
    generated_at: datetime
    metrics: list[DashboardMetric]
    open_support_tickets: int
    pending_partner_verifications: int
    active_alerts: int


class PartnerReviewRequest(BaseModel):
    decision: str = Field(pattern="^(approve|reject|request_changes)$")
    note: str = Field(min_length=3, max_length=1000)


class PartnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    partner_type: str
    legal_name: str
    verification_status: str
    commission_rate: Decimal
    payout_status: str

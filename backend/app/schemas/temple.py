from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TempleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    slug: str
    name: str
    deity: str | None
    category: str
    city: str
    state: str
    description: str
    latitude: Decimal
    longitude: Decimal
    rating: Decimal
    is_verified: bool


class CrowdResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    level: str
    queue_minutes: int
    observed_at: datetime
    source: str

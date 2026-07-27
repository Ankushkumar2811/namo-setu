from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    product_type: str = Field(pattern="^(hotel|dharamshala|cab|guide|puja|donation)$")
    product_id: UUID
    service_date: date
    amount_inr: Decimal = Field(ge=0, decimal_places=2)


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    reference: str
    product_type: str
    product_id: UUID
    status: str
    service_date: date
    amount_inr: Decimal
    created_at: datetime

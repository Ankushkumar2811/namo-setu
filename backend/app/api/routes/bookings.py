import secrets

from fastapi import APIRouter, Header, status
from sqlalchemy import select

from app.api.dependencies import CurrentUser, Session
from app.core.errors import DomainError
from app.models.entities import Booking
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreate,
    user: CurrentUser,
    session: Session,
    idempotency_key: str = Header(min_length=16, max_length=80, alias="Idempotency-Key"),
) -> BookingResponse:
    existing = await session.scalar(select(Booking).where(Booking.idempotency_key == idempotency_key))
    if existing:
        if existing.user_id != user.id:
            raise DomainError("idempotency_conflict", "Idempotency key belongs to another request", 409)
        return BookingResponse.model_validate(existing)
    booking = Booking(
        user_id=user.id,
        reference=f"NS{secrets.token_hex(6).upper()}",
        product_type=payload.product_type,
        product_id=payload.product_id,
        service_date=payload.service_date,
        amount_inr=payload.amount_inr,
        idempotency_key=idempotency_key,
    )
    session.add(booking)
    await session.flush()
    return BookingResponse.model_validate(booking)

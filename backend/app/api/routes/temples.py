from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.api.dependencies import Session
from app.core.errors import DomainError
from app.repositories.temples import TempleRepository
from app.schemas.common import Page, PageMeta
from app.schemas.temple import CrowdResponse, TempleResponse

router = APIRouter(prefix="/temples", tags=["Temples"])


@router.get("", response_model=Page[TempleResponse])
async def list_temples(
    session: Session,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    query: Annotated[str | None, Query(max_length=120)] = None,
    state: Annotated[str | None, Query(max_length=120)] = None,
) -> Page[TempleResponse]:
    repository = TempleRepository(session)
    items, total = await repository.list(query, state, (page - 1) * page_size, page_size)
    return Page(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))


@router.get("/{temple_id}", response_model=TempleResponse)
async def get_temple(temple_id: UUID, session: Session) -> TempleResponse:
    temple = await TempleRepository(session).by_id(temple_id)
    if temple is None:
        raise DomainError("temple_not_found", "Temple was not found", 404)
    return TempleResponse.model_validate(temple)


@router.get("/{temple_id}/crowd", response_model=CrowdResponse)
async def get_temple_crowd(temple_id: UUID, session: Session) -> CrowdResponse:
    crowd = await TempleRepository(session).latest_crowd(temple_id)
    if crowd is None:
        raise DomainError("crowd_unavailable", "Live crowd information is not available", 404)
    return CrowdResponse.model_validate(crowd)

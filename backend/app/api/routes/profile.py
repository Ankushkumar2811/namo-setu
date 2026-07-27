from pydantic import BaseModel, ConfigDict

from app.api.dependencies import CurrentUser

from fastapi import APIRouter

router = APIRouter(prefix="/profile", tags=["Profile"])


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    full_name: str
    role: str


@router.get("", response_model=ProfileResponse)
async def get_profile(user: CurrentUser) -> ProfileResponse:
    return ProfileResponse.model_validate(user)

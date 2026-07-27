from fastapi import APIRouter

from app.api.routes import admin, ai, auth, bookings, profile, temples

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(temples.router)
api_router.include_router(bookings.router)
api_router.include_router(ai.router)
api_router.include_router(admin.router)

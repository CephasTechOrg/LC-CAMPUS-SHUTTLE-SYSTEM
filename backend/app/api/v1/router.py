from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import auth, driver, health, routes, shuttles, stops, student, timetable

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(driver.router, prefix="/driver", tags=["driver"])
api_router.include_router(student.router, prefix="/student", tags=["student"])
api_router.include_router(stops.router, prefix="/stops", tags=["stops"])
api_router.include_router(routes.router, prefix="/routes", tags=["routes"])
api_router.include_router(shuttles.router, prefix="/shuttles", tags=["shuttles"])
api_router.include_router(timetable.router, prefix="/timetable", tags=["timetable"])

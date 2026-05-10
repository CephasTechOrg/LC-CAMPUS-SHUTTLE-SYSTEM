from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.constants import UserRole
from app.core.permissions import require_roles
from app.models.route import Route
from app.models.route_stop import RouteStop
from app.models.user import User
from app.repositories.route_repository import RouteRepository
from app.repositories.stop_repository import StopRepository
from app.schemas.route import RouteCreate, RouteRead, RouteStopCreate, RouteStopRead

router = APIRouter()


@router.get("", response_model=list[RouteRead])
async def list_routes(db: AsyncSession = Depends(get_db)):
    return await RouteRepository(db).list()


@router.post("", response_model=RouteRead, status_code=201)
async def create_route(
    payload: RouteCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    route = Route(**payload.model_dump())
    repo = RouteRepository(db)
    await repo.add(route)
    await db.commit()
    await db.refresh(route)
    return route


@router.post("/{route_id}/stops", response_model=RouteStopRead, status_code=201)
async def add_stop_to_route(
    route_id: UUID,
    payload: RouteStopCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    routes = RouteRepository(db)
    stops = StopRepository(db)

    route = await routes.get(route_id)
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found.")

    stop = await stops.get(payload.stop_id)
    if not stop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found.")

    route_stop = RouteStop(route_id=route_id, **payload.model_dump())
    await routes.add_route_stop(route_stop)
    await db.commit()
    await db.refresh(route_stop)
    return route_stop

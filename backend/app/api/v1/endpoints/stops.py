from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.constants import UserRole
from app.core.permissions import require_roles
from app.models.stop import Stop
from app.models.user import User
from app.repositories.stop_repository import StopRepository
from app.schemas.stop import StopCreate, StopRead, StopUpdate

router = APIRouter()


@router.get("", response_model=list[StopRead])
async def list_stops(db: AsyncSession = Depends(get_db)):
    return await StopRepository(db).list()


@router.post("", response_model=StopRead, status_code=201)
async def create_stop(
    payload: StopCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    stop = Stop(**payload.model_dump())
    repo = StopRepository(db)
    await repo.add(stop)
    await db.commit()
    await db.refresh(stop)
    return stop


@router.patch("/{stop_id}", response_model=StopRead)
async def update_stop(
    stop_id: UUID,
    payload: StopUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    repo = StopRepository(db)
    stop = await repo.get(stop_id)
    if not stop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found.")

    repo.apply_updates(stop, payload.model_dump(exclude_unset=True))
    await db.commit()
    await db.refresh(stop)
    return stop

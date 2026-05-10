from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.constants import UserRole
from app.core.permissions import require_roles
from app.models.shuttle import Shuttle
from app.models.user import User
from app.repositories.shuttle_repository import ShuttleRepository
from app.schemas.shuttle import ShuttleCreate, ShuttleRead, ShuttleUpdate

router = APIRouter()


@router.get("", response_model=list[ShuttleRead])
async def list_shuttles(db: AsyncSession = Depends(get_db)):
    return await ShuttleRepository(db).list()


@router.post("", response_model=ShuttleRead, status_code=201)
async def create_shuttle(
    payload: ShuttleCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    shuttle = Shuttle(**payload.model_dump())
    repo = ShuttleRepository(db)
    await repo.add(shuttle)
    await db.commit()
    await db.refresh(shuttle)
    return shuttle


@router.patch("/{shuttle_id}", response_model=ShuttleRead)
async def update_shuttle(
    shuttle_id: UUID,
    payload: ShuttleUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    repo = ShuttleRepository(db)
    shuttle = await repo.get(shuttle_id)
    if not shuttle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shuttle not found.")

    update_data = payload.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value

    repo.apply_updates(shuttle, update_data)
    await db.commit()
    await db.refresh(shuttle)
    return shuttle

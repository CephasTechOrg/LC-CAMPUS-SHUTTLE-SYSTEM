from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.constants import UserRole
from app.core.permissions import require_roles
from app.models.timetable import TimetableEntry
from app.models.user import User
from app.repositories.timetable_repository import TimetableRepository
from app.schemas.timetable import TimetableEntryCreate, TimetableEntryRead

router = APIRouter()


@router.get("", response_model=list[TimetableEntryRead])
async def list_timetable(db: AsyncSession = Depends(get_db)):
    return await TimetableRepository(db).list_active()


@router.post("", response_model=TimetableEntryRead, status_code=201)
async def create_timetable_entry(
    payload: TimetableEntryCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    entry = TimetableEntry(**payload.model_dump())
    repo = TimetableRepository(db)
    await repo.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry

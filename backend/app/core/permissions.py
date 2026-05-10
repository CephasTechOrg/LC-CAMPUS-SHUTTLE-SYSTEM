from __future__ import annotations

from fastapi import Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.constants import UserRole
from app.models.user import User


def require_roles(*allowed_roles: UserRole):
    async def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in {role.value for role in allowed_roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return dependency

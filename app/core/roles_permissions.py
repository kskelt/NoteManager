from app.dependencies.auth import IsAuthenticated
from app.models.permissions import Permission

from fastapi import Depends, HTTPException, status

from app.models.users import BaseUser

ROLE_PERMISSIONS = {
    "user": {
        Permission.CREATE_NOTE,
        Permission.READ_OWN_NOTE,
        Permission.UPDATE_OWN_NOTE,
        Permission.DELETE_NOTE,
    },
    "admin": {
        Permission.CREATE_NOTE,
        Permission.READ_OWN_NOTE,
        Permission.UPDATE_OWN_NOTE,
        Permission.DELETE_NOTE,
        Permission.READ_ALL_NOTES,
        Permission.READ_USER_NOTES,
        Permission.RESTORE_NOTE,
    },
}


def require_permission(permission: Permission):
    def dependency(auth: IsAuthenticated = Depends()):
        if permission not in ROLE_PERMISSIONS.get(auth.role, set()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return BaseUser(username=auth.login, role=auth.role)
    return dependency

from functools import wraps

from fastapi import Depends, HTTPException
from starlette import status

from core.users.exceptions import TokenIsNotValidException, UserAlreadyExistsException, ServiceError
from dependencies import get_current_user


def check_permission_decorator(required_permissions: list[str]):
    def decorator(func):
        @wraps
        async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            user_permissions = current_user.permissions
            if not set(required_permissions).issubset(set(user_permissions)):
                raise HTTPException(status_code=401, detail="Not enough permissions!")
            return await func(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator


def handle_user_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (UserAlreadyExistsException, TokenIsNotValidException, ServiceError) as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return wrapper

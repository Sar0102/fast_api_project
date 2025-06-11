from functools import wraps

from fastapi import HTTPException
from starlette import status

from core.exceptions import ProductAlreadyExistsError, ProductNotFoundError


def handle_product_errors(func):
    @wraps
    async def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ProductAlreadyExistsError, ProductNotFoundError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    return wrapper

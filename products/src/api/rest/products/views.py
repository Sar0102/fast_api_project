from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.rest.products.decorators import handle_product_errors
from core.products.services import product_service
from api.rest.users.decorators import check_permission_decorator
from dependencies import get_current_user
from core.permissions import Permissions

product_router = APIRouter(prefix='/products', tags=['Products'])


class Product(BaseModel):
    id: int
    name: str
    price: float


@product_router.post('')
@check_permission_decorator([Permissions.ADD_PRODUCT.value])
@handle_product_errors
async def create_products(
        product: Product,
        current_user=Depends(get_current_user),
):
    product_service.add(product)
    return {"message": f"Product {product.name} was added was created by {current_user.email}"}


@product_router.get('/{product_id}')
@check_permission_decorator([Permissions.VIEW_PRODUCT.value])
@handle_product_errors
async def get_products(
        product_id: int,
        current_user=Depends(get_current_user)
):
    product = product_service.get(product_id)
    return product


@product_router.put('/{product_id}')
@check_permission_decorator([Permissions.UPDATE_PRODUCT.value])
@handle_product_errors
async def update_products(
        product_id: int,
        product: Product,
        current_user=Depends(get_current_user)
):
    product_service.update(product_id, product)
    return {"message": f"Product was updated by {current_user.email}"}


@product_router.delete('/{product_id}')
@check_permission_decorator([Permissions.DELETE_PRODUCT.value])
@handle_product_errors
async def delete_products(
        product_id: int,
        current_user=Depends(get_current_user)
):
    product_service.delete(product_id)
    return {"message": f"Product was deleted by {current_user.email}"}

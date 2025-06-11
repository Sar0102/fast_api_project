from fastapi import APIRouter, Depends

from api.rest.decorators import handle_product_errors
from core.services import product_service
from core.transports import Product
from dependencies import get_current_user

product_router = APIRouter(prefix='/products', tags=['Products'])


@product_router.post('')
@handle_product_errors
async def create_products(
        product: Product,
        current_user=Depends(get_current_user),
):
    product_service.add(product)
    return {"message": f"Product {product.name} was added was created by {current_user.email}"}


@product_router.get('/{product_id}')
@handle_product_errors
async def get_products():
    product = product_service.list()
    return product


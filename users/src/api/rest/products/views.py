from fastapi import APIRouter, Depends

from api.rest.products.types import ProductCreate
from dependencies import get_current_user
from infrastructure.kafka.producer import send_product_creation_event
from infrastructure.product_service.product_facade import product_facade

products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.get("")
async def get_products(current_user=Depends(get_current_user)):
    return await product_facade.get_products()


@products_router.post("")
async def add_product(product: ProductCreate, current_user=Depends(get_current_user)):
    await send_product_creation_event(product)
    return {"message": "Task started!"}

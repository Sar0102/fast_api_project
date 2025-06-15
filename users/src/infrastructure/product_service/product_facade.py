from api.rest.products.types import ProductCreate
from infrastructure.external_service_facade import ExternalServiceFacade


class ProductFacade:

    def __init__(self, base_url: str):
        self.external_facade = ExternalServiceFacade(base_url)

    async def get_products(self) -> dict:
        return await self.external_facade.proxy_get(endpoint="products")

    async def add_product(self, product: ProductCreate):
        return await self.external_facade.proxy_post(endpoint="products", data=product.model_dump())


product_facade = ProductFacade(base_url="http://product_app:8000")
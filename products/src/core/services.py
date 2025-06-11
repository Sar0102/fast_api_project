from datetime import date, timedelta

import httpx

from core.transports import ProductHistory, Product, ProductCreate
from infrastructure.database.redis_repository import RedisRepository, redis_repository


class ProductService:

    def __init__(self, repository: RedisRepository):
        self.repository = repository


    @staticmethod
    async def get_usd_rates(day: date) -> float:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange",
                params={
                    "json": True,
                    "date": day.strftime("%Y%m%d"),
                }
            )
            usd_rate = next((item for item in response.json() if item['cc'] == 'USD'), {"rate": 0})
            return usd_rate['rate']

    async def add(self, product: ProductCreate):
        today = date.today()
        price_data = {}
        for i in range(7):
            day = today - timedelta(days=i)
            usd_rates = await self.get_usd_rates(day)
            price_data[day.strftime("%Y-%m-%d")] = usd_rates * product.origin_price

        history = ProductHistory(prices=price_data)
        product = Product(
            id=product.id,
            name=product.name,
            origin_price=product.price,
            price_history=history,
        )
        await self.repository.save(f"product_{product.id}", product)


    async def list(self):
        return await self.repository.list("product_*")

product_service = ProductService(redis_repository)
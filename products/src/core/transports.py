from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float

class Product(BaseModel):
    id: int
    name: str
    origin_price: float
    price_history: "ProductHistory"


class ProductHistory(BaseModel):
    prices: dict[str, float]
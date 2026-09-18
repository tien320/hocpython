from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class Product(BaseModel):
    product_id: int
    name: str
    price: Decimal
    stock: int
    created_at: date

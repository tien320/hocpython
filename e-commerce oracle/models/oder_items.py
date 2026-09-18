from pydantic import BaseModel
from decimal import Decimal

class OrderItem(BaseModel):
    order_id: int
    item_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from enum import Enum

class OrderStatus(str,Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(BaseModel):
    order_id: int
    customer_id: int
    total_amount: Decimal
    status: OrderStatus = OrderStatus.PENDING
    created_at: date    
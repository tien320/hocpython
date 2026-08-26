from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from repository import ProductRepository, OrderRepository
from services import OrderService
from database import init_db  # 1. Import hàm tạo bảng

# 2. Tạo bảng ngay khi nạp file main.py
init_db()

class CreateOrderRequest(BaseModel):
    product_id: int
    quantity: int

app = FastAPI()
product_repo = ProductRepository()
order_repo = OrderRepository()
order_service = OrderService(product_repo=product_repo, order_repo=order_repo)

# 3. Tạo sẵn 1 sản phẩm mẫu vào database nếu chưa có (để test không bị lỗi hết hàng)
if not product_repo.get_by_id(1):
    product_repo.create("Bàn phím cơ", 500000.0, 10)

@app.post("/orders", status_code=201)
def create_order(payload: CreateOrderRequest):
    order = order_service.place_order(product_id=payload.product_id, quantity=payload.quantity)
    if not order:
        raise HTTPException(status_code=400, detail="Sản phẩm không tồn tại hoặc không đủ hàng")
    return {
        "id": order.id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
        "status": order.status
    }
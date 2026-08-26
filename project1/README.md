Để tự tay code lại toàn bộ dự án từ đầu mà không cần chép mẫu, bạn hãy làm theo **Quy trình 5 bước tư duy kỹ thuật (Top-Down Thinking)**.

Mỗi khi bắt đầu một bài toán backend, bạn chỉ cần đặt ra các câu hỏi dưới đây cho từng tầng:

---

### 🗺️ BƯỚC 1: Tư duy Tầng Dữ liệu & Nghiệp vụ lõi (`models.py`)

**Câu hỏi tư duy:** _"Hệ thống này có những thực thể nào? Mỗi thực thể cần lưu thông tin gì và tự nó biết làm gì?"_

- **Thực thể 1: `Product**`
- **Thuộc tính:** Cần gì để mô tả 1 sản phẩm? $\rightarrow$ `id`, `name`, `price`, `stock`.
- **Phương thức:** Bản thân sản phẩm cần biết kiểm tra gì?
- Kiểm tra đủ hàng không: `is_available(self, quantity) -> bool`
- Tự trừ kho khi bán: `reduce_stock(self, quantity) -> None`

- **Thực thể 2: `Order**`
- **Thuộc tính:** Một đơn hàng gồm những gì? $\rightarrow$ `id`, `product_id`, `quantity`, `total_price`, `status`.

---

### 🗄️ BƯỚC 2: Quản lý Kết nối Database an toàn (`database.py`)

**Câu hỏi tư duy:** _"Làm sao để mở DB, dùng xong tự đóng/commit, gặp lỗi thì tự rollback?"_

- Dùng **Context Manager** của Python (`__enter__` và `__exit__`):
- Class `DatabaseConnection`:
- `__enter__`: Mở `sqlite3.connect()`, set `row_factory = sqlite3.Row`, trả về `conn`.
- `__exit__`: Nếu không lỗi $\rightarrow$ `conn.commit()`; nếu lỗi $\rightarrow$ `conn.rollback()`; cuối cùng luôn `conn.close()`.

- Viết thêm hàm tạo khung bảng rỗng: `init_db()` chứa câu SQL `CREATE TABLE IF NOT EXISTS...`.

---

### 📥 BƯỚC 3: Tư duy Tầng Truy xuất Dữ liệu (`repository.py`)

**Câu hỏi tư duy:** _"Tầng này chỉ làm đúng 1 việc: chạy SQL. Mỗi bảng cần những thao tác đọc/ghi nào?"_

- **`ProductRepository`:**
- Thêm mới: `create(self, name, price, stock) -> Product`
- Đọc 1 cái theo ID: `get_by_id(self, product_id) -> Product | None`
- Lấy danh sách toàn bộ: `get_all(self) -> list[Product]`
- Cập nhật tồn kho: `update_stock(self, new_stock, product_id) -> bool`

- **`OrderRepository`:**
- Lưu đơn hàng: `create(self, product_id, quantity, total_price, status) -> Order`

_(Quy tắc vàng: Mở kết nối `with self.db_factory() as conn:` $\rightarrow$ chạy SQL có dấu `?` $\rightarrow$ lấy kết quả và map ngược lại thành Object)._

---

### ⚙️ BƯỚC 4: Tư duy Tầng Xử lý Nghiệp vụ (`services.py`)

**Câu hỏi tư duy:** _"Khi người dùng bấm Mua hàng, quy trình logic gồm các bước tuần tự nào?"_

- Tạo class `OrderService` nhận vào 2 repository (`product_repo`, `order_repo`).
- Viết hàm `place_order(self, product_id, quantity)` theo luồng:

1. Gọi `product_repo.get_by_id(product_id)` để tìm sản phẩm.
2. Nếu không thấy $\rightarrow$ `return None`.
3. Gọi `product.is_available(quantity)` kiểm tra kho. Nếu không đủ $\rightarrow$ `return None`.
4. Tính `total_price = product.price * quantity`.
5. Gọi `product.reduce_stock(quantity)` để trừ kho trên RAM.
6. Gọi `product_repo.update_stock(...)` để ghi nhận số lượng mới vào DB.
7. Gọi `order_repo.create(...)` để lưu đơn hàng mới và trả về đối tượng `Order`.

---

### 🌐 BƯỚC 5: Tư duy Tầng Giao tiếp API (`main.py`)

**Câu hỏi tư duy:** _"Người dùng gửi dữ liệu gì lên? URL nào? Cần phản hồi mã lỗi gì?"_

1. **Khởi tạo:** Gọi `init_db()` để sẵn sàng database. Khởi tạo `app = FastAPI()`, các repo và service.
2. **Định nghĩa Schema (Pydantic):**

- `CreateProductRequest`: `name: str`, `price: float`, `stock: int`
- `CreateOrderRequest`: `product_id: int`, `quantity: int`

3. **Viết Endpoints:**

- `@app.post("/products", status_code=201)`: Nhận payload $\rightarrow$ gọi `product_repo.create` $\rightarrow$ trả về JSON.
- `@app.get("/products")`: Gọi `product_repo.get_all` $\rightarrow$ trả về danh sách JSON.
- `@app.post("/orders", status_code=201)`: Nhận payload $\rightarrow$ gọi `order_service.place_order` $\rightarrow$ nếu `None` thì `raise HTTPException(status_code=400)`, nếu có thì trả về thông tin đơn hàng.

---

### 🎯 Kế hoạch hành động cho bạn

1. Tạo một thư mục mới tinh (ví dụ `my_shop/`).
2. Tự tay tạo lần lượt 5 file: `models.py` $\rightarrow$ `database.py` $\rightarrow$ `repository.py` $\rightarrow$ `services.py` $\rightarrow$ `main.py`.
3. Viết đến đâu, viết một khối `if __name__ == "__main__":` ở cuối file đó để chạy thử và kiểm tra ngay.

# TaskForge Backend API

FastAPI RESTful Backend cho hệ thống quản lý công việc và dự án TaskForge, tích hợp cơ sở dữ liệu Oracle Database và kiến trúc đa tầng (Layered Clean Architecture).

---

## 🏛️ Kiến trúc hệ thống (Clean Architecture)

Backend được tổ chức tách biệt rõ ràng theo từng tầng trách nhiệm:

- **`api/v1/routers/`**: Định tuyến HTTP endpoints, tiếp nhận request và phản hồi dữ liệu (`auth`, `workspaces`, `projects`, `tasks`, `comments`, `users`).
- **`services/`**: Xử lý logic nghiệp vụ và kiểm tra quyền hạn (Role-based Authorization: OWNER, ADMIN, MEMBER).
- **`repositories/`**: Tầng truy xuất dữ liệu (Data Access Object / Repository Pattern) tương tác trực tiếp với cơ sở dữ liệu.
- **`models/`**: Khai báo các thực thể SQLAlchemy ORM (`entities.py`) và Enums trạng thái (`enums.py`).
- **`schema/`**: Pydantic schemas kiểm tra và định dạng dữ liệu đầu vào/ra (Data Validation & Serialization).
- **`core/`**: Cấu hình hệ thống (`config.py`), kết nối cơ sở dữ liệu (`database.py`), bảo mật JWT (`security.py`), ghi log (`logger.py`), và launcher tương thích Windows (`uvicorn_loop.py`).

---

## ⚙️ Cài đặt & Khởi chạy

### 1. Cài đặt thư viện

Sử dụng môi trường ảo của dự án:
```powershell
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường (`.env`)

Tạo file `.env` tại thư mục này với nội dung cấu hình Oracle DB:

```env
ORACLE_USER=system
ORACLE_PASSWORD=your_password
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XEPDB1

SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Đồng bộ cơ sở dữ liệu (Alembic)

```powershell
alembic upgrade head
```

### 4. Khởi chạy ứng dụng

Chạy file `run.py` từ thư mục này:

```powershell
python run.py
```

> **Lưu ý quan trọng trên Windows**:
> Driver bất đồng bộ của Oracle (`python-oracledb` async) yêu cầu `SelectorEventLoop`. Launcher `run.py` đã cấu hình vòng lặp này trước khi Uvicorn khởi động. Không nên dùng trực tiếp lệnh `uvicorn main:app` trên Windows.

### 5. Tài liệu API (Swagger UI)

Sau khi server khởi động:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

# hocpython

Kho bài tập và dự án thực hành Python, SQL (SQLite & Oracle Database), Phân tích dữ liệu (Pandas & ETL), Kiến trúc ứng dụng (Clean / Layered Architecture) và ứng dụng Fullstack (FastAPI + React).

---

## 📂 Nội dung repository

### 1. Dự án ứng dụng tiêu biểu

- **[`taskforge/`](taskforge/) (Fullstack Application)**: Hệ thống quản lý công việc và dự án theo nhóm với phân quyền người dùng (Owner, Admin, Member):
  - **[`projecttaskforge_backend/`](taskforge/projecttaskforge_backend/)**: RESTful API Backend xây dựng bằng **FastAPI**, kết nối **Oracle Database** thông qua **SQLAlchemy 2.0 (Async)** và `python-oracledb`, quản lý migration với **Alembic**, bảo mật JWT, thiết kế theo chuẩn Clean Architecture (Routers, Services, Repositories, Models, Schemas).
  - **[`projecttaskforge_frontend/`](taskforge/projecttaskforge_frontend/)**: Giao diện người dùng Single Page App (SPA) với **React 19** và **Vite**, quản lý xác thực qua Context API, tích hợp Axios và Vite proxy để gọi API backend.
- **[`quan li user oracle/`](quan%20li%20user%20oracle/)**: Hệ thống quản lý người dùng kết nối Oracle Database, mã hóa mật khẩu bcrypt, bảo mật JWT token, Alembic migration kèm Postman Collections và Environment.
- **[`e-commerce oracle/`](e-commerce%20oracle/)**: Mô hình quản lý đơn hàng và sản phẩm (E-commerce) với kết nối Oracle Database và Repository Pattern.
- **[`quan li user/`](quan%20li%20user/)**: Ứng dụng quản lý người dùng cơ bản theo mô hình phân tầng.
- **[`project mathang/`](project%20mathang/)**: Ứng dụng hướng đối tượng (OOP) quản lý mặt hàng, thiết bị điện tử, tích hợp FastAPI và SQLite.
- **[`project1/`](project1/)**: Ứng dụng quản lý sản phẩm và đơn hàng với SQLite, áp dụng Context Manager kết nối an toàn, phân tách Model - Repository - Service - API.
- **[`project2/sinhvienmanage/`](project2/sinhvienmanage/)**: Ứng dụng quản lý sinh viên hướng đối tượng.
- **[`project3/usermanage/`](project3/usermanage/)**: Ứng dụng quản lý người dùng dạng console/service.
- **[`projectreview/studentmanagement/`](projectreview/studentmanagement/)**: Dự án ôn tập OOP kế thừa và quản lý sinh viên (`Person`, `Student`).

### 2. SQL & Cơ sở dữ liệu

- **Thực hành SQLite với Python**:
  - `intro_sqlite3.py`, `crudsqlite3.py`: kết nối và thao tác CRUD cơ bản với SQLite.
  - `productionsqlite3.py`, `sytnaxsqlite3.py`: áp dụng Context Manager, xử lý transaction và bảo đảm an toàn kết nối.
- **Truy vấn SQL**:
  - `11-8.sql`, `crud.sql`, `crudnangcao.sql`: các bài tập CRUD và truy vấn SQL nâng cao.
  - `cte-subquery.sql`, `sql-subquery.sql`: kỹ thuật CTE (Common Table Expressions) và Subquery.
  - `logs/query_log.sql`: log các câu truy vấn thực hành.
- **Tài liệu tham khảo**: [lithuyetsql.md](lithuyetsql.md), [sqlite3.md](sqlite3.md), [singleton.md](singleton.md), [projectstructure.md](projectstructure.md).

### 3. Phân tích dữ liệu & ETL

- `hoc_pandas.py`: đọc, lọc, biến đổi và phân tích dữ liệu bằng Pandas.
- `readolist.py`: khám phá tập dữ liệu thương mại điện tử Olist.
- `baitoanetl.py`: bài tập xử lý luồng ETL.
- `pipeline.py`: pipeline đọc dữ liệu đơn hàng, làm sạch, join `orders` / `items` / `products` và tổng hợp doanh thu xuất kho theo ngày (`fact_outbound_daily.csv`).
- `olist/`: tập dữ liệu CSV gốc của Olist.

### 4. Bài tập Python & Thuật toán

- `syntax1.py` đến `syntax9.py`: chuỗi bài luyện cú pháp Python từ cơ bản đến nâng cao.
- `luyensyntax.py`, `300baicode.py`, `test.py`: bài tập giải thuật tổng hợp.
- `binarytree.py`, `linkedlist.py`: cấu trúc dữ liệu cây nhị phân và danh sách liên kết.
- `module1.py` đến `module4.py`: thực hành tách và tái sử dụng module.
- `lamsachchuoi.py`: xử lý và chuẩn hóa chuỗi dữ liệu.
- `leetcode/`: lời giải và phân tích các bài toán LeetCode.
- Tài liệu liên quan: [lithuyetpython.md](lithuyetpython.md), [chiasyntax.md](chiasyntax.md), [chiamodule.md](chiamodule.md).

---

## 🚀 Hướng dẫn khởi chạy

### 1. Kích hoạt môi trường ảo Python

```powershell
.\.venv\Scripts\Activate.ps1
# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 2. Chạy bài tập hoặc script đơn lẻ

```powershell
python syntax1.py
python pipeline.py
```

### 3. Khởi chạy hệ thống TaskForge (Fullstack)

**Backend:**
```powershell
cd taskforge\projecttaskforge_backend
# Cấu hình file .env theo thông tin Oracle DB
alembic upgrade head
python run.py
```
> Tài liệu Swagger API tại: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Frontend:**
```powershell
cd taskforge\projecttaskforge_frontend
npm install
npm run dev
```
> Truy cập giao diện web tại: [http://localhost:5173](http://localhost:5173)

### 4. Khởi chạy các project FastAPI khác

```powershell
cd "project mathang"
python main.py
```

---

## 📌 Ghi chú

- **Oracle Database**: Các project `taskforge`, `quan li user oracle` và `e-commerce oracle` yêu cầu cơ sở dữ liệu Oracle đang chạy. Hãy kiểm tra và khai báo chính xác thông tin đăng nhập trong file `.env` trước khi khởi chạy.
- **Windows Async Event Loop**: Trên hệ điều hành Windows, các backend dùng `python-oracledb` ở chế độ bất đồng bộ cần chạy qua launcher `run.py` (sử dụng `SelectorEventLoop`) để tránh xung đột với IOCP loop mặc định.
- **Dữ liệu ETL**: Script `pipeline.py` đọc dữ liệu từ thư mục `olist/`; nếu chuyển mã nguồn sang máy khác, hãy đảm bảo cấu hình đường dẫn dữ liệu phù hợp.

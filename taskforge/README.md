# TaskForge - Hệ Thống Quản Lý Không Gian Làm Việc, Dự Án & Công Việc (Fullstack)

TaskForge là hệ thống quản lý công việc và dự án theo mô hình cộng tác (team collaboration), hỗ trợ phân quyền chặt chẽ theo vai trò (Owner, Admin, Member), được xây dựng theo kiến trúc Clean Architecture với Backend FastAPI và Frontend React/Vite.

---

## 🏗️ Cấu trúc thư mục

```text
taskforge/
├── projecttaskforge_backend/   # RESTful API Backend (FastAPI + Oracle Database + SQLAlchemy)
└── projecttaskforge_frontend/  # Web Application Frontend (React 19 + Vite)
```

---

## ⚡ Công nghệ sử dụng

### Backend (`projecttaskforge_backend`)
- **Ngôn ngữ & Framework**: Python 3.12+, FastAPI
- **Database**: Oracle Database
- **ORM & Data Access**: SQLAlchemy 2.0 (Async), `python-oracledb`
- **Database Migration**: Alembic
- **Xác thực & Bảo mật**: JWT (JSON Web Tokens), OAuth2 Password Bearer, Passlib/Bcrypt
- **Validation**: Pydantic v2
- **Event Loop**: Windows Selector Event Loop (tương thích async Oracle driver trên Windows)

### Frontend (`projecttaskforge_frontend`)
- **Thư viện UI**: React 19, Vite
- **HTTP Client**: Axios (interceptor tự động gắn Bearer Token)
- **State Management**: React Context API (`AuthContext`)
- **Giao diện**: Custom CSS hiện đại, tối ưu trải nghiệm người dùng

---

## 🚀 Tính năng chính

1. **Authentication & User Management**:
   - Đăng ký, đăng nhập nhận JWT Token.
   - Lấy thông tin cá nhân (`/auth/me`), cập nhật hồ sơ người dùng.
2. **Workspaces & Membership**:
   - Tạo và quản lý Workspace (người tạo tự động làm `OWNER`).
   - Mời, phân quyền thành viên (`ADMIN`, `MEMBER`) và xóa thành viên khỏi workspace.
3. **Projects**:
   - Tạo và quản lý dự án bên trong từng Workspace.
   - Cập nhật, xóa và truy xuất thông tin dự án.
4. **Tasks / Issues**:
   - Tạo task, giao task (`assignee`), đặt mức độ ưu tiên (`priority`).
   - Cập nhật trạng thái task (`TODO`, `IN_PROGRESS`, `DONE`, ...).
   - Lọc và tìm kiếm task theo trạng thái, người được giao, từ khóa và phân trang.
5. **Comments**:
   - Bình luận theo luồng trong từng task.
   - Quyền tác giả: chỉ cho phép người viết hoặc Admin chỉnh sửa/xóa bình luận.

---

## 🛠️ Hướng dẫn cài đặt & Khởi chạy

### 1. Khởi chạy Backend

1. Di chuyển vào thư mục backend:
   ```powershell
   cd taskforge\projecttaskforge_backend
   ```
2. Cấu hình biến môi trường trong file `.env`:
   ```env
   ORACLE_USER=your_user
   ORACLE_PASSWORD=your_password
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE_NAME=XEPDB1
   SECRET_KEY=your_secret_key
   ```
3. Chạy migration cơ sở dữ liệu:
   ```powershell
   alembic upgrade head
   ```
4. Khởi chạy server bằng launcher `run.py`:
   ```powershell
   python run.py
   ```
   > **Lưu ý**: Trên Windows, cần chạy qua `run.py` thay vì `uvicorn main:app` để kích hoạt Selector Event Loop phù hợp với driver bất đồng bộ của Oracle.

5. Truy cập Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Khởi chạy Frontend

1. Di chuyển vào thư mục frontend:
   ```powershell
   cd taskforge\projecttaskforge_frontend
   ```
2. Cài đặt các gói phụ thuộc:
   ```bash
   npm install
   ```
3. Khởi chạy server phát triển:
   ```bash
   npm run dev
   ```
4. Mở trình duyệt tại địa chỉ hiển thị trên terminal (mặc định: [http://localhost:5173](http://localhost:5173)). Frontend đã cấu hình proxy tự động chuyển tiếp request `/api/v1` về backend cổng `8000`.

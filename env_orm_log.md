### 1. ENV (Environment Variables - Biến môi trường)

**Khái niệm:**

ENV là các cặp khóa - giá trị (`KEY=VALUE`) được lưu trữ bên ngoài mã nguồn, nằm ở cấp độ hệ điều hành hoặc file cấu hình cục bộ (như `.env`).

**Dùng để làm gì?**

- **Bảo mật:** Tránh để lộ thông tin nhạy cảm (mật khẩu DB, JWT Secret Key, API Key) khi đẩy code lên Git/GitHub.
- **Tách biệt môi trường:** Dễ dàng chuyển đổi cấu hình giữa môi trường Phát triển (`Development`), Kiểm thử (`Staging`), và Thực tế (`Production`) mà không cần sửa code.

**Cách hoạt động:**

1. Các biến được nạp vào bộ nhớ tiến trình (Process Memory) khi ứng dụng khởi chạy.
2. Thư viện (như `python-dotenv` hoặc `pydantic-settings`) đọc file `.env` và gắn vào `os.environ`.
3. Code đọc giá trị trực tiếp từ hệ thống: `os.getenv("DB_PASSWORD")` hoặc thông qua object `settings.DB_PASSWORD`.

---

### 2. LOG (Logging - Ghi nhật ký hệ thống)

**Khái niệm:**

Log là cơ chế ghi lại toàn bộ lịch sử hoạt động, trạng thái và lỗi của ứng dụng theo thời gian thực vào console hoặc file lưu trữ.

**Dùng để làm gì?**

- **Điều tra sự cố (Debugging / Tracing):** Biết chính xác lỗi xảy ra ở đâu, vào lúc nào và với dữ liệu nào mà không làm gián đoạn chương trình.
- **Giám sát hệ thống:** Theo dõi hành vi người dùng (ví dụ: đăng nhập thất bại liên tục, lưu lượng truy cập bất thường).
- **Thay thế hoàn toàn `print()`:** `print()` chỉ hiển thị tạm thời trên console, không lưu vết, không có mốc thời gian và không phân loại được mức độ nghiêm trọng.

**Cách hoạt động & Phân cấp (Log Levels):**

- Hệ thống xử lý thông điệp qua bộ lọc cấp độ ưu tiên:
- **DEBUG:** Thông tin chi tiết phục vụ lập trình viên tìm lỗi.
- **INFO:** Xác nhận luồng chạy bình thường (ví dụ: "Đã kết nối DB", "Tạo user thành công").
- **WARNING:** Cảnh báo bất thường nhưng chưa làm dừng hệ thống (ví dụ: "Email đã tồn tại", "Bộ nhớ sắp đầy").
- **ERROR:** Có lỗi xảy ra khiến một chức năng thất bại (ví dụ: không thể ghi dữ liệu, lỗi cú pháp truy vấn).
- **CRITICAL:** Lỗi nghiêm trọng khiến toàn bộ ứng dụng dừng hoạt động (ví dụ: sập DB, hết dung lượng đĩa cứng).

- Logger tự động gắn nhãn: `[Thời gian] - [Level] - [Tên file:Dòng code] - [Nội dung log]` và chuyển tới file/console.

---

### 3. ORM (Object-Relational Mapping)

**Khái niệm:**

ORM là kỹ thuật cầu nối giúp ánh xạ các bảng quan hệ trong cơ sở dữ liệu thành các lớp (Classes/Objects) trong ngôn ngữ lập trình hướng đối tượng.

**Dùng để làm gì?**

- **Viết code theo tư duy OOP:** Thao tác với dữ liệu thông qua thuộc tính và phương thức của object (`user.name = "An"`) thay vì ghép nối chuỗi SQL thô.
- **Chống SQL Injection:** Tự động tham số hóa (parameterize) dữ liệu đầu vào.
- **Độc lập cơ sở dữ liệu:** Cùng một cú pháp ORM có thể chạy trên Oracle, PostgreSQL, MySQL hoặc SQLite chỉ bằng việc đổi chuỗi kết nối.
- **Tự động hóa Migration:** Đồng bộ các thay đổi cấu trúc bảng trực tiếp từ code Python xuống DB.

**Cách hoạt động (Vòng đời dữ liệu):**

1. **Model Mapping:** Khai báo một Class tương ứng với cấu trúc 1 Bảng (thuộc tính của class là các cột).
2. **Identity Map & State Tracking (Session):** Session theo dõi trạng thái của từng object (New, Dirty/Modified, Deleted, Clean).
3. **Unit of Work & SQL Compilation:** Khi gọi `flush()` hoặc `commit()`, ORM tự động dịch các thay đổi của object thành các câu lệnh SQL tối ưu (`INSERT`, `UPDATE`, `DELETE`) và thực thi xuống Database engine.

---

### Bảng tổng hợp vai trò trong kiến trúc dự án

| Thành phần | Vị trí trong hệ thống               | Trả lời cho câu hỏi                                           | Lợi ích cốt lõi                               |
| ---------- | ----------------------------------- | ------------------------------------------------------------- | --------------------------------------------- |
| **ENV**    | Tầng cấu hình (Configuration)       | _"Ứng dụng đang chạy ở đâu, với thông số bảo mật nào?"_       | Bảo mật, linh hoạt cấu hình theo từng máy chủ |
| **LOG**    | Tầng quan sát (Observability)       | _"Hệ thống đang chạy ra sao, có vấn đề gì bất thường không?"_ | Truy vết sự cố, giám sát vận hành thực tế     |
| **ORM**    | Tầng truy cập dữ liệu (Persistence) | _"Dữ liệu được đọc/ghi và biểu diễn trong code như thế nào?"_ | An toàn dữ liệu, code gọn gàng, chuẩn OOP     |

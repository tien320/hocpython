**Chỉ mục (Index)** trong cơ sở dữ liệu là một **cấu trúc dữ liệu phụ** (thường là B-Tree hoặc Hash) được lưu trữ tách biệt với bảng chính. Nhiệm vụ duy nhất của nó là **tăng tốc độ tìm kiếm và truy xuất dữ liệu**, giúp Database định vị chính xác vị trí dòng dữ liệu cần lấy mà không cần duyệt qua toàn bộ bảng.

---

### 1. Bản chất & Tương quan dễ hiểu

- **Ví dụ thực tế:** Index giống như **Mục lục** ở đầu cuốn sách.
- Nếu không có mục lục, muốn tìm bài viết về _"Cấu trúc B-Tree"_, bạn phải lật từng trang từ 1 đến 500 (**Full Table Scan**).
- Có mục lục, bạn tra từ khóa $\rightarrow$ biết ngay bài đó nằm ở trang 235 $\rightarrow$ mở thẳng đến trang 235 (**Index Scan**).

---

### 2. Ưu điểm và Đánh đổi (Trade-off)

- **Ưu điểm:**
- Giảm thời gian thực thi câu lệnh `SELECT` từ hàng vài giây/phút xuống còn vài millisecond.
- Tối ưu hiệu năng cho các phép toán `WHERE`, `JOIN`, `ORDER BY`, `GROUP BY` và các câu lệnh hàm cửa sổ (`Window Functions`).

- **Đánh đổi (Nhược điểm):**
- **Tốn dung lượng lưu trữ:** Cần thêm bộ nhớ/đĩa cứng để lưu cây Index.
- **Làm chậm các thao tác Ghi (`INSERT`, `UPDATE`, `DELETE`):** Mỗi khi dữ liệu bảng chính biến động, Database phải tốn tài nguyên tính toán để cập nhật lại cấu trúc cây Index.

---

### 3. Hai loại Index cốt lõi

1. **Clustered Index (Chỉ mục cụm):**

- Sắp xếp và **lưu trữ dữ liệu thực sự** của bảng theo thứ tự của Index.
- **Đặc điểm:** Mỗi bảng **chỉ có duy nhất 1** Clustered Index (thường tự động gắn liền với `PRIMARY KEY`).

2. **Non-Clustered Index (Chỉ mục phi cụm / Secondary Index):**

- Lưu giá trị của cột được đánh index kèm theo **con trỏ (Pointer)** trỏ về vị trí dòng dữ liệu tương ứng ở bảng chính.
- **Đặc điểm:** Một bảng có thể tạo **nhiều** Non-Clustered Index (`CREATE INDEX...`).

---

### 4. Quy tắc "Vàng" khi làm việc với Index

- **Nên đánh Index khi:** Cột thường xuyên xuất hiện ở mệnh đề `WHERE`, điều kiện `JOIN`, `ORDER BY`, hoặc có độ đa dạng dữ liệu cao (High Cardinality - như Email, Mã định danh, ID).
- **Không nên đánh Index khi:** Bảng quá nhỏ, cột có độ đa dạng thấp (như Giới tính, Trạng thái Active/Inactive), hoặc bảng chịu tần suất `INSERT`/`UPDATE` liên tục.
- **Những cạm bẫy làm "Phế" Index (Index Invalidation):**
- Bị bọc bởi hàm: `WHERE YEAR(created_at) = 2026` ❌ $\rightarrow$ Đổi thành: `WHERE created_at >= '2026-01-01'`
- Tìm kiếm chuỗi có `%` ở đầu: `WHERE name LIKE '%An'` ❌
- Ép kiểu ngầm định hoặc thực hiện phép toán trên cột: `WHERE price * 2 > 100` ❌

---

### 5. Ba câu lệnh SQL bạn cần nhớ

```sql
-- 1. Tạo Index
CREATE INDEX idx_users_email ON users(email);

-- 2. Kiểm tra câu lệnh có dùng Index hay không
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@gmail.com';

-- 3. Xóa Index khi không dùng đến
DROP INDEX idx_users_email;

```

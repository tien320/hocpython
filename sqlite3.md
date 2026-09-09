Mọi thao tác với SQLite trong Python đều xoay quanh 3 khái niệm cốt lõi:

- **Connection (`conn`)**: Cầu nối mở file database.
- **Cursor (`cursor`)**: "Con trỏ" gửi lệnh SQL và nhận kết quả về.
- **`commit()`**: Xác nhận lưu thay đổi vào đĩa cứng (bắt buộc khi Thêm/Sửa/Xóa).

Tạo một file chạy thử độc lập (ví dụ `test_db.py`) và thực hành theo từng bước dưới đây.

---

**1. Kết nối và tạo bảng (Create Table)**

```python
import sqlite3

# 1. Kết nối (nếu file chưa có, SQLite tự tạo file test.db)
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# 2. Tạo bảng sinh viên với các kiểu dữ liệu cơ bản
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gpa REAL NOT NULL
    )
""")

# 3. Lưu thay đổi và đóng tạm kết nối
conn.commit()
print("-> Đã tạo bảng thành công!")

```

_Các kiểu dữ liệu chính trong SQLite:_

- `INTEGER`: Số nguyên (`student_id`, `age`).
- `REAL`: Số thực (`gpa`).
- `TEXT`: Chuỗi ký tự (`name`).
- `PRIMARY KEY`: Khóa chính, tự động chặn trùng lặp ID.

---

**2. Thêm dữ liệu (Create - INSERT)**

Luôn dùng dấu `?` làm placeholder để truyền biến vào câu SQL, tránh lỗi cú pháp và lỗ hổng SQL Injection.

```python
# Thêm 1 dòng dữ liệu
student_data = (1, "Lê Bật Tiến", 21, 3.6)

try:
  cursor.execute(
      """
        INSERT INTO students (student_id, name, age, gpa)
        VALUES (?, ?, ?, ?)
    """,
      student_data,
  )

  conn.commit()  # Bắt buộc phải commit thì dữ liệu mới lưu xuống file
  print("-> Đã thêm dữ liệu thành công!")
except sqlite3.IntegrityError:
  print("Lỗi: ID này đã tồn tại trong database!")

```

---

**3. Đọc dữ liệu (Read - SELECT)**

Khi SELECT, không cần dùng `conn.commit()`. Dùng `fetchall()` để lấy toàn bộ danh sách, hoặc `fetchone()` để lấy 1 dòng.

```python
# Lấy toàn bộ danh sách
cursor.execute("SELECT student_id, name, age, gpa FROM students")
all_rows = cursor.fetchall()  # Trả về list of tuples

print("\n--- DANH SÁCH SINH VIÊN ---")
for row in all_rows:
  # row là một tuple: (1, 'Lê Bật Tiến', 21, 3.6)
  print(f"ID: {row[0]} | Tên: {row[1]} | Tuổi: {row[2]} | GPA: {row[3]}")

# Tìm 1 người theo ID
find_id = 1
cursor.execute(
    "SELECT student_id, name, age, gpa FROM students WHERE student_id = ?",
    (find_id,),
)
single_row = cursor.fetchone()

if single_row:
  print(f"\nTìm thấy ID {find_id}: Tên là {single_row[1]}")
else:
  print("\nKhông tìm thấy!")

```

---

**4. Sửa dữ liệu (Update - UPDATE)**

```python
new_gpa = 3.8
target_id = 1

cursor.execute(
    """
    UPDATE students
    SET gpa = ?
    WHERE student_id = ?
""",
    (new_gpa, target_id),
)

conn.commit()
print(f"-> Đã cập nhật GPA cho sinh viên {target_id}!")

```

---

**5. Xóa dữ liệu (Delete - DELETE)**

```python
delete_id = 1

cursor.execute(
    """
    DELETE FROM students
    WHERE student_id = ?
""",
    (delete_id,),
)

conn.commit()

# Kiểm tra xem có dòng nào thực sự bị xóa không
if cursor.rowcount > 0:
  print(f"-> Đã xóa thành công sinh viên có ID {delete_id}!")
else:
  print("Không tìm thấy ID để xóa.")

# Đóng kết nối khi hoàn tất chương trình
conn.close()

```

---

**Bảng tổng hợp cú pháp cốt lõi**

| Thao tác              | Cú pháp SQL cơ bản                      | Phương thức trong Python            | Cần `commit()`? |
| --------------------- | --------------------------------------- | ----------------------------------- | --------------- |
| **Kết nối**           | Không                                   | `conn = sqlite3.connect("file.db")` | Không           |
| **Tạo bảng**          | `CREATE TABLE IF NOT EXISTS ...`        | `cursor.execute(...)`               | Có              |
| **Thêm (Create)**     | `INSERT INTO table VALUES (?, ?)`       | `cursor.execute(sql, (val1, val2))` | **Có**          |
| **Đọc tất cả (Read)** | `SELECT * FROM table`                   | `cursor.fetchall()`                 | Không           |
| **Đọc 1 dòng (Read)** | `SELECT * FROM table WHERE id = ?`      | `cursor.fetchone()`                 | Không           |
| **Sửa (Update)**      | `UPDATE table SET cot = ? WHERE id = ?` | `cursor.execute(sql, (val, id))`    | **Có**          |
| **Xóa (Delete)**      | `DELETE FROM table WHERE id = ?`        | `cursor.execute(sql, (id,))`        | **Có**          |

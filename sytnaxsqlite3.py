import sqlite3

# 1. KẾT NỐI VÀ TẠO BẢNG
conn = sqlite3.connect("app_data.db")  # Tự tạo file nếu chưa tồn tại
cursor = conn.cursor()

# Tạo bảng mẫu
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER
)
""")
conn.commit()


# 2. CREATE (Thêm bản ghi)
# Luôn dùng dấu ? làm tham số để chống lỗi SQL Injection
sql_insert = "INSERT INTO users (name, email, age) VALUES (?, ?, ?)"

# Thêm 1 dòng
cursor.execute(sql_insert, ("Nguyen Van A", "a@example.com", 25))

# Thêm nhiều dòng cùng lúc
danh_sach = [
    ("Tran Thi B", "b@example.com", 22),
    ("Le Van C", "c@example.com", 30),
]
cursor.executemany(sql_insert, danh_sach)
conn.commit()


# 3. READ (Đọc dữ liệu)
# Lấy toàn bộ danh sách
cursor.execute("SELECT * FROM users")
all_users = cursor.fetchall()
print("Toàn bộ danh sách:")
for user in all_users:
    print(user)

# Lấy 1 bản ghi kèm điều kiện lọc
cursor.execute("SELECT id, name, age FROM users WHERE email = ?", ("a@example.com",))
user_a = cursor.fetchone()
print(f"Chi tiết user A: {user_a}")


# 4. UPDATE (Cập nhật dữ liệu)
sql_update = "UPDATE users SET age = ? WHERE email = ?"
cursor.execute(sql_update, (26, "a@example.com"))
conn.commit()


# 5. DELETE (Xóa dữ liệu)
sql_delete = "DELETE FROM users WHERE email = ?"
cursor.execute(sql_delete, ("c@example.com",))
conn.commit()


# 6. ĐÓNG KẾT NỐI
cursor.close()
conn.close()
# python_fix_script.py
with open("Chinook_Oracle.sql", "r", encoding="utf-8") as f:
    text = f.read()

# Chuyển cú pháp gộp VALUES (...), (...) thành từng lệnh INSERT riêng
# Đổi các dòng dạng "    (123, " thành "INSERT INTO ... VALUES (123, "
lines = text.split("\n")
new_lines = []
current_insert_prefix = ""

for line in lines:
    stripped = line.strip()
    if stripped.startswith("INSERT INTO"):
        # Lưu lại câu lệnh INSERT INTO Table (Cols) VALUES
        current_insert_prefix = line.split("VALUES")[0] + "VALUES "
        new_lines.append(line)
    elif stripped.startswith("(") and current_insert_prefix:
        # Nếu là dòng chứa dữ liệu tiếp theo
        clean_line = stripped.rstrip(",")
        if clean_line.endswith(";"):
            clean_line = clean_line[:-1]
            current_insert_prefix = "" # Kết thúc khối insert
        
        if not line.strip().startswith("INSERT"):
            new_lines.append(current_insert_prefix + clean_line + ";")
        else:
            new_lines.append(clean_line + ";")
    else:
        new_lines.append(line)

with open("Chinook_Oracle_Fixed.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("Đã tạo xong file Chinook_Oracle_Fixed.sql chuẩn cú pháp Oracle!")
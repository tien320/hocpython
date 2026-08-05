import re

# Đọc file SQL gốc
with open(r'Chinook_Oracle.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Trích xuất phần CREATE TABLE (từ "Create Tables" đến "Populate Tables")
match = re.search(r'/\*+\s*Create Tables\s*\*+/([\s\S]*?)/\*+\s*Populate Tables', content, re.IGNORECASE)
if match:
    create_section = match.group(1)
else:
    create_section = ""

# Xóa các lệnh GRANT và CONNECT
create_section = re.sub(r'GRANT\s+.*?;', '', create_section, flags=re.IGNORECASE)
create_section = re.sub(r'CONNECT\s+.*?;', '', create_section, flags=re.IGNORECASE)

# Thêm phần CREATE FOREIGN KEYS nếu có
fk_match = re.search(r'/\*+\s*Create Foreign Keys\s*\*+/([\s\S]*?)(?=/\*|$)', content, re.IGNORECASE)
fk_section = ""
if fk_match:
    fk_section = fk_match.group(1)

header = """/*******************************************************************************
   Chinook Database - Create Tables Only
   Chạy file này trước tiên để tạo tất cả các bảng
   Sau đó chạy: Chinook_Insert_Only.sql để INSERT dữ liệu
********************************************************************************/

"""

final_content = header + create_section + fk_section

# Ghi file mới
with open('Chinook_Create_Only.sql', 'w', encoding='utf-8') as f:
    f.write(final_content)

print('✓ Tạo file CREATE TABLE: Chinook_Create_Only.sql')

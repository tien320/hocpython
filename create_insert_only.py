import re

# Đọc file SQL gốc
with open(r'Chinook_Oracle.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Trích xuất chỉ phần từ "Populate Tables" đến cuối
match = re.search(r'/\*+\s*Populate Tables\s*\*+/([\s\S]*)', content, re.IGNORECASE)
if match:
    insert_section = match.group(1)
else:
    insert_section = content

# Xử lý các lỗi
# Pattern 1: 'text1 '||chr(38)||' text2' => 'text1 & text2'
def replace_concat_ampersand(match):
    before = match.group(1)
    after = match.group(2)
    return f"'{before} & {after}'"

insert_section = re.sub(r"'([^']*?)'\s*\|\|chr\(38\)\|\|\s*'([^']*?)'", replace_concat_ampersand, insert_section)

# Pattern 2: 'text1'||chr(39)||'text2' => 'text1''text2'
def replace_concat_quote(match):
    before = match.group(1)
    after = match.group(2)
    return f"'{before}''{after}'"

insert_section = re.sub(r"'([^']*?)'\s*\|\|chr\(39\)\|\|\s*'([^']*?)'", replace_concat_quote, insert_section)

# Xóa single chr(38) và chr(39) còn lại
insert_section = insert_section.replace('chr(38)', "'&'")
insert_section = insert_section.replace('chr(39)', "''")

# Thêm header
header = """/*******************************************************************************
   Chinook Database - Data Insert Only
   Đã sửa lỗi chr(38) và chr(39) để tương thích với DBeaver/Oracle
   Chỉ chứa phần INSERT INTO
   Chạy file này SAU khi đã tạo xong các bảng (CREATE TABLE)
********************************************************************************/

"""

final_content = header + insert_section

# Ghi file mới
with open('Chinook_Insert_Only.sql', 'w', encoding='utf-8') as f:
    f.write(final_content)

print('✓ Tạo file INSERT ONLY: Chinook_Insert_Only.sql')

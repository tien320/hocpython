import re

def fix_and_extract_inserts(input_file, output_file):
    # Các bảng cần lấy
    target_tables = ['EMPLOYEE', 'CUSTOMER', 'INVOICE', 'INVOICELINE']
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Sửa lỗi ghép chuỗi '||chr(39)||' thành dấu nháy đơn kép ''
    content = content.replace("'||chr(39)||'", "''")
    content = content.replace("'||chr(38)||'", "&")

    # 2. Tách thành từng câu lệnh SQL (phân tách bởi dấu chấm phẩy)
    raw_statements = content.split(';')
    
    cleaned_inserts = []

    for stmt in raw_statements:
        stmt_clean = stmt.strip()
        
        # Chỉ xử lý các câu lệnh INSERT INTO
        if stmt_clean.upper().startswith('INSERT INTO'):
            
            # Kiểm tra câu lệnh thuộc 1 trong 4 bảng yêu cầu
            match_table = re.search(r'INSERT\s+INTO\s+(\w+)', stmt_clean, re.IGNORECASE)
            if match_table:
                table_name = match_table.group(1).upper()
                
                if table_name in target_tables:
                    # Sửa lỗi đúp "INSERT INTO Table VALUES INSERT INTO Table VALUES (...)"
                    # Chỉ giữ lại phần từ "INSERT INTO Table ... VALUES (...)"
                    first_values_idx = stmt_clean.upper().find('VALUES')
                    if first_values_idx != -1:
                        # Lấy lại định dạng chuẩn: INSERT INTO TableName (...) VALUES (...)
                        header = stmt_clean[:first_values_idx + 6]
                        body = stmt_clean[first_values_idx + 6:]
                        
                        # Loại bỏ các đoạn header trùng lặp nếu có ở phần body
                        body = re.sub(r'INSERT\s+INTO\s+\w+\s*(\([^)]+\))?\s*VALUES', '', body, flags=re.IGNORECASE)
                        
                        final_stmt = header + ' ' + body.strip()
                        
                        # Sửa định dạng Date string thành TO_DATE chuẩn Oracle nếu có
                        final_stmt = re.sub(
                            r"'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})'", 
                            r"TO_DATE('\1 \2', 'YYYY-MM-DD HH24:MI:SS')", 
                            final_stmt
                        )
                        final_stmt = re.sub(
                            r"'(\d{4}-\d{2}-\d{2})'", 
                            r"TO_DATE('\1', 'YYYY-MM-DD')", 
                            final_stmt
                        )
                        
                        cleaned_inserts.append(final_stmt + ";")

    # 3. Ghi kết quả ra file SQL sạch
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- ======================================================\n")
        f.write("-- SCRIPT KHẮC PHỤC LỖI INSERT CHO 4 BẢNG CHINfilter\n")
        f.write("-- ======================================================\n\n")
        f.write("\n".join(cleaned_inserts))
        f.write("\n\nCOMMIT;\n")

    print(f"Đã xử lý xong! Lọc và làm sạch được {len(cleaned_inserts)} câu lệnh INSERT vào file '{output_file}'.")

# Chạy hàm (Đổi tên file input nếu cần)
fix_and_extract_inserts('Chinook_Oracle_Fixed.sql', 'chinook_4_tables_inserts.sql')
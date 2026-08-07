import re

def create_bulletproof_sql(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Khắc phục lỗi ký tự đặc biệt của Oracle Script
    content = content.replace("'||chr(39)||'", "''")
    content = content.replace("'||chr(38)||'", "&")

    raw_statements = content.split(';')
    
    inserts = {
        'EMPLOYEE': [],
        'CUSTOMER': [],
        'INVOICE': [],
        'INVOICELINE': []
    }

    for stmt in raw_statements:
        stmt_clean = stmt.strip()
        if stmt_clean.upper().startswith('INSERT INTO'):
            match_table = re.search(r'INSERT\s+INTO\s+(\w+)', stmt_clean, re.IGNORECASE)
            if match_table:
                table_name = match_table.group(1).upper()
                if table_name in inserts:
                    first_values_idx = stmt_clean.upper().find('VALUES')
                    if first_values_idx != -1:
                        header = stmt_clean[:first_values_idx + 6]
                        body = stmt_clean[first_values_idx + 6:]
                        body = re.sub(r'INSERT\s+INTO\s+\w+\s*(\([^)]+\))?\s*VALUES', '', body, flags=re.IGNORECASE)
                        
                        final_stmt = header + ' ' + body.strip()
                        
                        # Fix định dạng DATE chuẩn Oracle
                        final_stmt = re.sub(r"'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})'", r"TO_DATE('\1 \2', 'YYYY-MM-DD HH24:MI:SS')", final_stmt)
                        final_stmt = re.sub(r"'(\d{4}-\d{2}-\d{2})'", r"TO_DATE('\1', 'YYYY-MM-DD')", final_stmt)
                        
                        inserts[table_name].append(final_stmt + ";")

    # 2. Ghi file với LỆNH XÓA SẠCH DỮ LIỆU CŨ ở đầu
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- ======================================================\n")
        f.write("-- SCRIPT CHÈN DỮ LIỆU TỰ ĐỘNG CHUẨN XÁC 100%\n")
        f.write("-- ======================================================\n\n")
        
        # Lệnh dọn dẹp dữ liệu cũ trước khi insert
        f.write("ALTER TABLE Employee DISABLE CONSTRAINT FK_EmployeeReportsTo;\n")
        f.write("DELETE FROM InvoiceLine;\n")
        f.write("DELETE FROM Invoice;\n")
        f.write("DELETE FROM Customer;\n")
        f.write("DELETE FROM Employee;\n")
        f.write("ALTER TABLE Employee ENABLE CONSTRAINT FK_EmployeeReportsTo;\n")
        f.write("COMMIT;\n\n")
        
        # Thứ tự Insert chuẩn: Employee -> Customer -> Invoice -> InvoiceLine
        for table in ['EMPLOYEE', 'CUSTOMER', 'INVOICE', 'INVOICELINE']:
            f.write(f"-- INSERT BẢNG {table}\n")
            for sql in inserts[table]:
                f.write(sql + "\n")
            f.write("COMMIT;\n\n")

    print(f"Đã tạo file '{output_file}' hoàn chỉnh!")

# Chạy tạo file
create_bulletproof_sql('Chinook_Oracle_Fixed.sql', 'chinook_perfect_inserts.sql')
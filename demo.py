import csv
import json
from datetime import datetime

# ==============================================================================
# HÀM BỔ TRỢ: LÀM SẠCH VÀ CHUẨN HÓA DỮ LIỆU (TRANSFORM)
# ==============================================================================

def lam_sach_chuoi(val):
    """Xóa khoảng trắng thừa ở đầu/cuối và chuẩn hóa chuỗi rỗng"""
    if not val:
        return ""
    return val.strip()

def chuan_hoa_ngay(date_str):
    """
    Thử chuyển đổi nhiều định dạng ngày bẩn về chuẩn ISO 8601 (YYYY-MM-DD)
    Nếu không thể parse được -> Trả về None để ghi nhận dữ liệu thiếu/hỏng
    """
    date_str = lam_sach_chuoi(date_str)
    if not date_str:
        return None
    
    # Danh sách các định dạng ngày bẩn thường gặp
    formats = ["%d/%m/%Y", "%Y-%m-%d", "%Y.%m.%d", "%d-%m-%Y"]
    
    for fmt in formats:
        try:
            # Parse chuỗi thành đối tượng datetime của Python
            dt = datetime.strptime(date_str, fmt)
            # Format lại về chuẩn quốc tế ISO 8601 YYYY-MM-DD
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue # Nếu sai định dạng thì thử định dạng tiếp theo
            
    return None # Nếu thử hết tất cả định dạng mà vẫn lỗi

def chuan_hoa_so_thuc(num_str):
    """Ép kiểu sang float an toàn, nếu lỗi trả về 0.0"""
    try:
        return float(lam_sach_chuoi(num_str))
    except (ValueError, TypeError):
        return 0.0

# ==============================================================================
# PIPELINE CHÍNH: EXTRACT -> TRANSFORM -> LOAD
# ==============================================================================

def etl_csv_to_json(input_csv, output_json):
    clean_data = []
    so_dong_loi = 0
    so_dong_thanh_cong = 0

    print(f"--- BẮT ĐẦU XỬ LÝ FILE: {input_csv} ---")

    # 1. EXTRACT: Đọc file CSV bằng try-except an toàn
    try:
        with open(input_csv, mode='r', encoding='utf-8') as f_csv:
            reader = csv.DictReader(f_csv)
            
            # 2. TRANSFORM: Duyệt từng dòng bằng cơ chế Streaming (Tiết kiệm RAM)
            for idx, row in enumerate(reader, start=2): # Dòng 1 là Header
                try:
                    # a. Làm sạch chuỗi
                    id_user = lam_sach_chuoi(row.get("ID"))
                    ho_ten = lam_sach_chuoi(row.get("HoTen"))
                    
                    # Skip dòng nếu thiếu thông tin quan trọng nhất (Primary Key / Name)
                    if not id_user or not ho_ten:
                        print(f"[Cảnh báo] Dòng {idx}: Thiếu ID hoặc Họ Tên -> Bỏ qua.")
                        so_dong_loi += 1
                        continue

                    # b. Chuẩn hóa ngày sinh và điểm số
                    ngay_sinh_clean = chuan_hoa_ngay(row.get("NgaySinh"))
                    diem_clean = chuan_hoa_so_thuc(row.get("DiemTichLuy"))

                    # c. Đóng gói dữ liệu đã làm sạch vào Dict
                    record = {
                        "id": id_user,
                        "ho_ten": ho_ten,
                        "ngay_sinh": ngay_sinh_clean, # Dạng "YYYY-MM-DD" hoặc None
                        "diem_tich_luy": diem_clean
                    }
                    
                    clean_data.append(record)
                    so_dong_thanh_cong += 1

                except Exception as e:
                    print(f"[Lỗi Dòng {idx}] Không thể xử lý dữ liệu: {e}")
                    so_dong_loi += 1

    except FileNotFoundError:
        print(f"[Lỗi Hệ Thống] Không tìm thấy file đầu vào: '{input_csv}'")
        return
    except UnicodeDecodeError:
        print(f"[Lỗi Mã Hóa] File '{input_csv}' không phải chuẩn UTF-8!")
        return

    # 3. LOAD: Xuất dữ liệu đã làm sạch ra file JSON
    try:
        with open(output_json, mode='w', encoding='utf-8') as f_json:
            json.dump(clean_data, f_json, indent=4, ensure_ascii=False)
            
        print("\n--- KẾT QUẢ XỬ LÝ ---")
        print(f"✅ Đã xử lý thành công : {so_dong_thanh_cong} dòng")
        print(f"⚠️ Bị bỏ qua/Lỗi dữ liệu: {so_dong_loi} dòng")
        print(f"🎉 Đã xuất file JSON sạch tại: {output_json}")

    except PermissionError:
        print(f"[Lỗi Ghi File] Không có quyền ghi file ra '{output_json}'.")

# ==============================================================================
# CHẠY THỬ NGHIỆM TẠO FILE DỮ LIỆU BẨN VÀ XỬ LÝ
# ==============================================================================

# Tạo file CSV bẩn để test
raw_content = """ID,HoTen,NgaySinh,DiemTichLuy
US01,   Nguyễn Văn A   ,15/08/1998,8.5
US02,Trần Thị B,1995-12-20,N/A
,Lê Không ID,2000.01.01,9.0
US04, Hoàng Nam ,31-02-2021,7.2
"""

with open('raw_users.csv', 'w', encoding='utf-8') as f:
    f.write(raw_content)

# Chạy Pipeline
etl_csv_to_json('raw_users.csv', 'clean_users.json')
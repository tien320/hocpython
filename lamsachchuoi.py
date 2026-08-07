import csv
import json
from datetime import datetime
def lam_sach_chuoi(val):
    if not val:
        return ''
    else: 
        return val.strip()

def chuan_hoa_ngay(date_str):
    date_str = lam_sach_chuoi(date_str)
    if not date_str:
        return None
    formats = ["%d/%m/%Y", "%Y-%m-%d", "%Y.%m.%d", "%d-%m-%Y"]
    for format in formats:
        try:
            dt = datetime.strptime(date_str, format)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None
def chuan_hoa_so_thuc(num_str):
    try:
        return float(lam_sach_chuoi(num_str))
    except(ValueError,TypeError):
        return 0
def etl_csv_to_json(input_csv,output_json):
    clean_data = []
    so_dong_loi = 0
    so_dong_thanh_cong = 0
    try:
        with open('input.csv',mode='r',encoding='utf-8') as f_csv:
            reader = csv.DictReader(f_csv)
        for idx,row in enumerate(reader,start=2):
            try:
                id_user = lam_sach_chuoi(row.get("ID"))
                ho_ten = lam_sach_chuoi(row.get("HoTen"))
                if not id_user or not ho_ten:
                    print(f"[Cảnh báo] Dòng {idx}: Thiếu ID hoặc Họ Tên -> Bỏ qua.")
                    so_dong_loi +=1
                    continue
                ngay_sinh_clean = chuan_hoa_ngay(row.get("NgaySinh"))
                diem_clean = chuan_hoa_so_thuc(row.get("DiemTichluy"))
                record ={
                    "ID" : id_user,
                    "ho_ten" : ho_ten,
                    "ngay_sinh" : ngay_sinh_clean,
                    "diem_tich_luy" : diem_clean
                }
                clean_data.append(record)
                so_dong_thanh_cong +=1
            except Exception as e:
                print(f"[Lỗi Dòng {idx}] Không thể xử lý dữ liệu: {e}")
                so_dong_loi += 1
    except FileNotFoundError:
        print(f"[Lỗi Hệ Thống] Không tìm thấy file đầu vào: '{input_csv}'")
        return
    except UnicodeDecodeError:
        print(f"[Lỗi Mã Hóa] File '{input_csv}' không phải chuẩn UTF-8!")
        return
    try:
        with open('output_json',mode='w',encoding='utf-8') as f_json:
            json.dump(clean_data,f_json,indent=4,ensure_ascii=False)
        print("\n--- KẾT QUẢ XỬ LÝ ---")
        print(f"✅ Đã xử lý thành công : {so_dong_thanh_cong} dòng")
        print(f"⚠️ Bị bỏ qua/Lỗi dữ liệu: {so_dong_loi} dòng")
        print(f"🎉 Đã xuất file JSON sạch tại: {output_json}")

    except PermissionError:
        print(f"[Lỗi Ghi File] Không có quyền ghi file ra '{output_json}'.")

# ==============================================================================
# BƯỚC 1: TẠO FILE CSV BẨN TRƯỚC (BẮT BUỘC ĐẶT TRÊN)
# ==============================================================================
raw_content = """ID,HoTen,NgaySinh,DiemTichLuy
US01,   Nguyễn Văn A   ,15/08/1998,8.5
US02,Trần Thị B,1995-12-20,N/A
,Lê Không ID,2000.01.01,9.0
US04, Hoàng Nam ,31-02-2021,7.2
"""

# Ghi đoạn text trên ra file 'raw_users.csv'
with open('raw_users.csv', mode='w', encoding='utf-8') as f:
    f.write(raw_content)

print("--> Đã tạo xong file raw_users.csv thô!")

# ==============================================================================
# BƯỚC 2: MỚI GỌI HÀM ETL ĐỂ ĐỌC VÀ LÀM SẠCH FILE VỪA TẠO (ĐẶT Ở DƯỚI)
# ==============================================================================
etl_csv_to_json('raw_users.csv', 'clean_users.json')
import csv
import json
#bai1
products = [
    {"id": "P01", "name": "Bàn phím cơ", "price": 1200000, "quantity": 15},
    {"id": "P02", "name": "Chuột không dây", "price": 450000, "quantity": 30},
    {"id": "P03", "name": "Màn hình 24 inch", "price": 3200000, "quantity": 8}
]
with open('products.json', mode = 'w', encoding='utf-8') as p_json:
    json.dump(products, p_json, indent=4, ensure_ascii=False)
with open('products.csv', mode = 'w', encoding= 'utf-8') as p_csv:
    cac_cot = ['id', 'name', 'price', 'quantity']
    writer = csv.DictWriter(p_csv, fieldnames=cac_cot)
    writer.writerows(products)
    writer.writeheader()
with open('products.json',mode='r',encoding='utf-8') as f_json:
    data_load = json.load(f_json)
total = 0
for product in products:
    total += product['price'] * product['quantity']
print(total)
#bai2
import csv
import json
raw_csv_content = [
    ["MaSV", "HoTen", "Toan", "Van", "Anh"],
    ["SV01", "Nguyễn Văn An", "8.5", "7.0", "9.0"],
    ["SV02", "Trần Thị Bích", "6.0", "8.5", "8.0"],
    ["SV03", "Lê Hoàng Nam", "9.0", "9.0", "9.5"]
]
with open('raw_csv_content.csv',mode='w',newline='',encoding='utf-8') as f_csv:
    writer = csv.writer(f_csv)
    writer.writerows(raw_csv_content)
doi_kieu = []
with open('raw_csv_content.csv',mode='r',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        toan = float(row['Toan'])
        van = float(row['Van'])
        anh = float(row['Anh'])
        diem_tb = round((toan+van+anh)/3,2)
        student_dict = {
            'MaSV' : row['MaSV'],
            'Hoten': row['HoTen'],
            'Toan' : toan,
            'Van' : van,
            'Anh' : anh,
            'Diem_tb' : diem_tb
        }
        doi_kieu.append(student_dict)
with open('doi_kieu.json',mode='w',encoding='utf-8') as f_json:
    json.dump(doi_kieu,f_json,indent=4,ensure_ascii=False)
print('da doi')
#bai3
import csv
import json

raw_logs_json = '''[
    {"id": "TX101", "user": "An", "items": ["Sách", "Bút"], "total": 150000, "status": "success"},
    {"id": "TX102", "user": "Bình", "items": ["Tai nghe"], "total": 500000, "status": "failed"},
    {"id": "TX103", "user": "An", "items": ["Vở", "Bao thư", "Thước"], "total": 85000, "status": "success"}
]'''
logs = json.loads(raw_logs_json)
giao_dich_thanh_cong =[]
for log in logs:
    if log['status'] == "success":
       items_str = ",".join(log['items']) 
       giao_dich_thanh_cong.append({
           'id' : log['id'],
           'user' : log['user'],
           'items' : items_str,
           'total' : log['total'],
           'status' : log['status']
       })
with open('thanh_cong.csv',mode='w',newline='',encoding='utf-8') as f_csv:
    field_name = ['id','user','items','total','status']
    writer = csv.DictWriter(f_csv,fieldnames=field_name)
    writer.writeheader()
    writer.writerows(giao_dich_thanh_cong)
print('thanh cong')
#ngoai le
#bai1
import json

def doc_config(file_path):
    # Cấu hình mặc định dùng làm phương án dự phòng (Fallback)
    default_config = {"theme": "light", "language": "vi"}
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            config_data = json.load(f)
            print("--> Đọc file cấu hình thành công!")
            return config_data

    except FileNotFoundError:
        # Lỗi 1: Không tìm thấy file trên ổ cứng
        print(f"[Cảnh báo] File '{file_path}' không tồn tại! Dùng cấu hình mặc định.")
        return default_config

    except json.JSONDecodeError as e:
        # Lỗi 2: File có tồn tại nhưng nội dung JSON bị sai cú pháp
        print(f"[Cảnh báo] File '{file_path}' bị hỏng cấu trúc (Dòng {e.lineno})! Dùng cấu hình mặc định.")
        return default_config

# --- THỬ NGHIỆM ---
# 1. Thử với file không tồn tại
config1 = doc_config("config_khong_ton_tai.json")
print("Kết quả 1:", config1)
#bai2
import csv

def doc_diem_csv(file_path):
    danh_sach_hop_le = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row_index, row in enumerate(reader, start=2): # start=2 vì dòng 1 là Header
                try:
                    # Ép kiểu dữ liệu - ĐÂY LÀ NƠI DỄ XẢY RA LỖI ValueError
                    diem_so = float(row['Diem'])
                    
                    danh_sach_hop_le.append({
                        "MaSV": row['MaSV'],
                        "HoTen": row['HoTen'],
                        "Diem": diem_so
                    })
                    
                except ValueError:
                    # Bắt lỗi ép kiểu riêng cho TỪNG DÒNG. 
                    # Vòng lặp 'for' bên ngoài KHÔNG BỊ DỪNG!
                    print(f"[Bỏ qua] Dòng {row_index}: Sinh viên '{row['HoTen']}' có điểm '{row['Diem']}' không phải là số hợp lệ.")

    except FileNotFoundError:
        print(f"[Lỗi Hệ Thống] Không tìm thấy file CSV tại '{file_path}'.")
    except PermissionError:
        print(f"[Lỗi Hệ Thống] File '{file_path}' đang bị mở bởi phần mềm khác (ví dụ: Excel). Hãy đóng lại!")
    except Exception as e:
        print(f"[Lỗi Bất Ngờ] {e}")

    return danh_sach_hop_le

# --- TẠO FILE VÀ THỬ NGHIỆM ---
# Tạo file test chứa dữ liệu lỗi
with open('test_diem.csv', mode='w', newline='', encoding='utf-8') as f:
    f.write("MaSV,HoTen,Diem\nSV01,Nguyễn Văn An,8.5\nSV02,Trần Thị Bích,ABC\nSV03,Lê Hoàng Nam,9.0\n")

print("--- BẮT ĐẦU ĐỌC FILE CSV ---")
ket_qua = doc_diem_csv('test_diem.csv')
print("Danh sách hợp lệ thu được:", ket_qua)
#bai3
import json

# 1. Tự định nghĩa Exception riêng đại diện cho Lỗi Nghiệp Vụ
class InvalidTransactionError(Exception):
    """Ngoại lệ riêng khi giao dịch trong hệ thống bị sai quy tắc nghiệp vụ."""
    pass

# 2. Hàm đọc và kiểm tra giao dịch
def kiem_tra_giao_dich(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            tx = json.load(f)
            
            # KIỂM TRA QUY TẮC NGHIỆP VỤ:
            if tx.get("so_tien", 0) <= 0:
                # Chủ động KÍCH HOẠT (raise) lỗi Custom Exception
                raise InvalidTransactionError(f"Số tiền giao dịch không hợp lệ ({tx.get('so_tien')} VNĐ). Số tiền phải > 0!")
            
            return tx

    except FileNotFoundError:
        print("[Lỗi System] File giao dịch không tồn tại.")
    except json.JSONDecodeError:
        print("[Lỗi System] File giao dịch không đúng cấu trúc JSON.")

# 3. CHƯƠNG TRÌNH CHÍNH (Giao diện gọi hàm và hứng Custom Exception)
# Tạo file JSON giả lập giao dịch âm tiền
data_test = {"id": "TX1001", "so_tien": -50000, "trang_thai": "success"}
with open('giao_dich_loi.json', 'w', encoding='utf-8') as f:
    json.dump(data_test, f)

print("--- PHÂN TÍCH GIAO DỊCH ---")
try:
    # Gọi hàm xử lý
    result = kiem_tra_giao_dich('giao_dich_loi.json')
    if result:
        print("Giao dịch hợp lệ:", result)
        
except InvalidTransactionError as e:
    # Hứng trực tiếp lỗi nghiệp vụ vừa tự tạo ở trên
    print(f"[Xử Lý Nghiệp Vụ] Giao dịch bị từ chối! Lý do: {e}")
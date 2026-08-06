import csv  # Thư viện chuẩn để thao tác với file CSV
import json # Thư viện chuẩn để thao tác với dữ liệu/file JSON

# ==============================================================================
# PHẦN 1: TẠO VÀ GHI DỮ LIỆU BẰNG CSV & JSON
# ==============================================================================

# Dữ liệu mẫu ban đầu dạng Danh sách các Dictionary (thường gặp trong thực tế)
danh_sach_hoc_sinh = [
    {"MaSV": "SV01", "HoTen": "Nguyễn Văn A", "Diem": 8.5, "MonHoc": ["Toán", "Lý"]},
    {"MaSV": "SV02", "HoTen": "Trần Thị B", "Diem": 9.0, "MonHoc": ["Văn", "Anh"]},
    {"MaSV": "SV03", "HoTen": "Lê Hoàng C", "Diem": 7.0, "MonHoc": ["Sử", "Địa"]}
]

# --- 1.1. GHI VÀO FILE JSON ---
# Mở file 'hoc_sinh.json' ở chế độ ghi ('w'), dùng utf-8 để không bị lỗi tiếng Việt
with open('hoc_sinh.json', mode='w', encoding='utf-8') as f_json:
    # json.dump(): Chuyển dict/list Python thành JSON và ghi thẳng vào file
    # indent=4: Tự động xuống dòng và lùi lề 4 dấu cách cho đẹp mắt
    # ensure_ascii=False: Bắt buộc có để giữ nguyên ký tự tiếng Việt (không bị biến thành \u00e0...)
    json.dump(danh_sach_hoc_sinh, f_json, indent=4, ensure_ascii=False)


# --- 1.2. GHI VÀO FILE CSV (Dùng DictWriter) ---
# Danh sách cột cho file CSV (JSON có thể chứa list, nhưng CSV chỉ nên lưu chuỗi/số)
data_csv = [
    {"MaSV": "SV01", "HoTen": "Nguyễn Văn A", "Diem": 8.5},
    {"MaSV": "SV02", "HoTen": "Trần Thị B", "Diem": 9.0},
    {"MaSV": "SV03", "HoTen": "Lê Hoàng C", "Diem": 7.0}
]

# Mở file CSV để ghi. CHÚ Ý: newline='' là BẮT BUỘC để tránh bị chèn dòng trống thừa trên Windows
with open('hoc_sinh.csv', mode='w', newline='', encoding='utf-8') as f_csv:
    cac_cot = ["MaSV", "HoTen", "Diem"] # Định nghĩa danh sách tên các cột (Header)
    
    # Tạo đối tượng writer dành cho Dictionary
    writer = csv.DictWriter(f_csv, fieldnames=cac_cot)
    
    writer.writeheader()  # Bước 1: Ghi dòng tiêu đề vào file CSV
    writer.writerows(data_csv) # Bước 2: Ghi toàn bộ danh sách dict vào các dòng tương ứng


# ==============================================================================
# PHẦN 2: ĐỌC VÀ XỬ LÝ DỮ LIỆU TỪ FILE CSV & JSON
# ==============================================================================

print("=== 2.1. ĐỌC TỪ FILE JSON ===")
# Mở file JSON ở chế độ đọc ('r')
with open('hoc_sinh.json', mode='r', encoding='utf-8') as f_json:
    # json.load(): Đọc nội dung file JSON và tự động chuyển về dạng list/dict trong Python
    data_loaded_json = json.load(f_json)
    
    # Lúc này data_loaded_json đã là một list các dictionary trong Python
    for hs in data_loaded_json:
        print(f"Mã: {hs['MaSV']} - Tên: {hs['HoTen']} - Các môn: {', '.join(hs['MonHoc'])}")


print("\n=== 2.2. ĐỌC TỪ FILE CSV DẠNG LIST (csv.reader) ===")
# Mở file CSV ở chế độ đọc
with open('hoc_sinh.csv', mode='r', encoding='utf-8') as f_csv:
    # csv.reader(): Trả về đối tượng duyệt từng dòng dưới dạng danh sách các chuỗi (list of strings)
    reader = csv.reader(f_csv)
    
    header = next(reader) # Đọc dòng đầu tiên để lấy tên cột (đồng thời bỏ qua nó trong vòng lặp)
    print("Tiêu đề cột:", header)
    
    for row in reader:
        # row[0]: MaSV, row[1]: HoTen, row[2]: Diem (tất cả đều đang ở dạng string)
        print(f"Học sinh: {row[1]} - Điểm: {float(row[2])}") # Tự ép kiểu float nếu cần tính toán


print("\n=== 2.3. ĐỌC TỪ FILE CSV DẠNG DICT (csv.DictReader) ===")
with open('hoc_sinh.csv', mode='r', encoding='utf-8') as f_csv:
    # csv.DictReader(): Lấy dòng đầu làm key, các dòng sau trả về kiểu dict giúp dễ đọc code
    dict_reader = csv.DictReader(f_csv)
    
    for row in dict_reader:
        # Lấy giá trị trực tiếp thông qua tên cột thay vì dùng chỉ số [0], [1]
        print(f"Mã SV: {row['MaSV']} -> Điểm: {row['Diem']}")


# ==============================================================================
# PHẦN 3: THAO TÁC VỚI CHUỖI JSON TRONG BỘ NHỚ (dumps & loads)
# ==============================================================================

# Khi giao tiếp API hoặc lưu vào DB, ta thường làm việc với Chuỗi JSON (JSON String) thay vì File

cai_dat_py = {"theme": "dark", "notifications": True, "volume": 80}

# --- 3.1. DUMPS (Dictionary -> JSON String) ---
# Chữ 's' cuối từ là viết tắt của String
json_string = json.dumps(cai_dat_py) 
print("\n=== 3.1. Chuỗi JSON được mã hóa từ Dict ===")
print(type(json_string)) # Trả về <class 'str'>
print(json_string)        # Kết quả: {"theme": "dark", "notifications": true, "volume": 80}

# --- 3.2. LOADS (JSON String -> Dictionary) ---
chuoi_json_input = '{"status": "success", "code": 200}'
dict_parsed = json.loads(chuoi_json_input)
print("\n=== 3.2. Chuyển từ chuỗi JSON về lại Dict ===")
print(type(dict_parsed))  # Trả về <class 'dict'>
print("Status code:", dict_parsed["code"])
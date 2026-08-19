import pandas as pd
import numpy as np

# ==============================================================================
# 1. KHOẢI TẠO VÀ XEM DỮ LIỆU CƠ BẢN (Initialization & Inspection)
# ==============================================================================
print("=== 1. TẠO VÀ XEM DỮ LIỆU MẪU ===")

# Tạo dữ liệu giả lập có chứa lỗi (khuyết thiếu, trùng lặp, sai định dạng)
raw_data = {
    'Ma_NV': ['NV01', 'NV02', 'NV03', 'NV04', 'NV05', 'NV05', 'NV06'],
    'Ten': ['An', 'Bình', 'Cường', 'Dũng', 'Giang', 'Giang', 'Hoa'],
    'Phong_Ban': ['IT', 'Sale', 'IT', 'HR', 'Sale', 'Sale', 'IT'],
    'Luong': [1500, 1200, np.nan, 900, 1100, 1100, 2000], # NV03 bị thiếu lương
    'Ngay_Vao_Lam': ['2021-01-15', '2020-05-10', '2022-03-01', '2019-11-20', '2021-08-15', '2021-08-15', '2023-01-10'],
    'Danh_Gia': ['A', 'B', 'A', 'C', 'B', 'B', np.nan]
}

# Tạo DataFrame
df = pd.DataFrame(raw_data)

# Xem 3 dòng đầu
print("\n--- df.head(3) ---")
print(df.head(3))

# Xem thông tin cấu trúc (Kiểu dữ liệu, số lượng null)
print("\n--- df.info() ---")
df.info()

# Xem thống kê nhanh các cột số
print("\n--- df.describe() ---")
print(df.describe())


# ==============================================================================
# 2. TRUY XUẤT VÀ LỌC DỮ LIỆU (Indexing & Filtering)
# ==============================================================================
print("\n=== 2. TRUY XUẤT & LỌC DỮ LIỆU ===")

# Lấy 1 cột (Trả về Series)
ten_series = df['Ten']

# Lấy nhiều cột (Trả về DataFrame)
thong_tin_luong = df[['Ten', 'Luong']]

# Dùng loc (lọc theo Tên/Điều kiện) và iloc (lọc theo Chỉ số vị trí)
print("\n--- Dùng iloc: Lấy 3 dòng đầu, 2 cột đầu ---")
print(df.iloc[0:3, 0:2])

print("\n--- Dùng loc: Lọc Nhân viên phòng IT có Lương > 1000 ---")
dieukien_it_luong = (df['Phong_Ban'] == 'IT') & (df['Luong'] > 1000)
df_it_cao = df.loc[dieukien_it_luong, ['Ma_NV', 'Ten', 'Luong']]
print(df_it_cao)


# ==============================================================================
# 3. LÀM SẠCH DỮ LIỆU (Data Cleaning)
# ==============================================================================
print("\n=== 3. LÀM SẠCH DỮ LIỆU ===")

# 3.1. Trùng lặp (Duplicates)
print(f"Số dòng trùng lặp: {df.duplicated().sum()}")
df = df.drop_duplicates().reset_index(drop=True) # Xóa dòng trùng và reset lại chỉ số
print("Đã xóa dòng trùng lặp 'NV05'.")

# 3.2. Ep kiểu dữ liệu (Data Type Conversion)
df['Ngay_Vao_Lam'] = pd.to_datetime(df['Ngay_Vao_Lam'])

# 3.3. Xử lý giá trị khuyết (Missing Values / NaN)
print("\nSố lượng NaN ở mỗi cột:")
print(df.isna().sum())

# Điền Lương thiếu bằng Lương trung bình của cả công ty
luong_tb = df['Luong'].mean()
df['Luong'] = df['Luong'].fillna(luong_tb)

# Điền Đánh giá thiếu bằng giá trị mặc định 'Chua_Danh_Gia'
df['Danh_Gia'] = df['Danh_Gia'].fillna('Chua_Danh_Gia')

print("\n--- DataFrame sau khi làm sạch ---")
print(df)


# ==============================================================================
# 4. BIẾN ĐỔI DỮ LIỆU (Data Transformation)
# ==============================================================================
print("\n=== 4. BIẾN ĐỔI DỮ LIỆU ===")

# 4.1. Tạo cột mới dựa trên tính toán
df['Luong_Thuong'] = df['Luong'] * 1.1

# 4.2. Dùng apply() với hàm Lambda để xếp loại
df['Cap_Bac'] = df['Luong'].apply(lambda x: 'Senior' if x >= 1500 else 'Junior')

# 4.3. Dùng map() để ánh xạ giá trị
anh_xa_danh_gia = {'A': 'Xuất sắc', 'B': 'Tốt', 'C': 'Trung bình', 'Chua_Danh_Gia': 'Không xác định'}
df['Mo_Ta_Danh_Gia'] = df['Danh_Gia'].map(anh_xa_danh_gia)

print(df[['Ten', 'Luong', 'Luong_Thuong', 'Cap_Bac', 'Mo_Ta_Danh_Gia']])


# ==============================================================================
# 5. GOM NHÓM & TỔNG HỢP DỮ LIỆU (Groupby & Aggregation)
# ==============================================================================
print("\n=== 5. GOM NHÓM (GROUPBY) ===")

# Tính Lương trung bình và Số lượng nhân viên theo từng Phòng ban
bang_phong_ban = df.groupby('Phong_Ban').agg(
    So_Luong=('Ma_NV', 'count'),
    Luong_Trung_Binh=('Luong', 'mean'),
    Luong_Cao_Nhat=('Luong', 'max')
).reset_index()

print(bang_phong_ban)


# ==============================================================================
# 6. GỘP BẢNG & TRỤC XOAY (Merge & Pivot Table)
# ==============================================================================
print("\n=== 6. GỘP BẢNG & PIVOT TABLE ===")

# 6.1. Merge (Tương tự SQL JOIN)
df_phu_cap = pd.DataFrame({
    'Phong_Ban': ['IT', 'Sale', 'HR'],
    'Phu_Cap_An_Trua': [500, 400, 300]
})

df_final = pd.merge(df, df_phu_cap, on='Phong_Ban', how='left')
print("\n--- Kết quả Merge với bảng Phụ Cấp ---")
print(df_final[['Ten', 'Phong_Ban', 'Luong', 'Phu_Cap_An_Trua']])

# 6.2. Pivot Table (Bảng tổng hợp 2 chiều)
pivot = df.pivot_table(
    index='Phong_Ban', 
    columns='Cap_Bac', 
    values='Ma_NV', 
    aggfunc='count', 
    fill_value=0
)
print("\n--- Pivot Table: Đếm số lượng nhân viên theo Phòng ban và Cấp bậc ---")
print(pivot)


# ==============================================================================
# 7. XUẤT DỮ LIỆU (Output)
# ==============================================================================
# df_final.to_csv('ket_qua_bai_lam.csv', index=False, encoding='utf-8-sig')
# df_final.to_excel('ket_qua_bai_lam.xlsx', index=False, engine='openpyxl')
print("\n=== HOÀN THÀNH QUY TRÌNH XỬ LÝ PANDAS ===")
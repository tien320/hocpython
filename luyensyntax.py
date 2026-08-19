import pandas as pd
import numpy as np

# Tạo dữ liệu thô (Raw data)
data = {
    'ma_phong': ['P101', 'P102', 'P103', 'P201', 'P202', 'P203', 'P301'],
    'loai_phong': ['Standard', 'VIP', 'Standard', 'VIP', 'Standard', 'VIP', 'Standard'],
    'ngay_thue': ['2023-01-15', '15/02/2023', 'invalid_date', '2023-11-20', '2024-01-05', '2024/02/10', None],
    'gia_thue': ['3000000', '5000000', None, '5500000', '3200000', 'NaN', '3100000'],
    'so_dien_tieu_thu': [120, np.nan, 95, 210, np.nan, 180, 105]
}
# Bài tập 1: Ép kiểu dữ liệu (Type Casting)

# Cột ngay_thue đang có nhiều định dạng khác nhau và có cả chuỗi lỗi ('invalid_date'). 
# Hãy ép kiểu cột này về dạng datetime. 
# Các giá trị bị lỗi hãy ép chúng thành NaT (Not a Time).

# Cột gia_thue đang bị hiểu là dạng chuỗi (object) thay vì số, 
# và chứa các giá trị như None, 'NaN'.
# Hãy ép kiểu cột này về dạng numeric (float).
df_phongtro = pd.DataFrame(data)
df_phongtro['ngay_thue'] = pd.to_datetime(df_phongtro['ngay_thue'].astype(str).str.strip(),format='mixed',errors="coerce",dayfirst=True)
df_phongtro['gia_thue'] = pd.to_numeric(df_phongtro['gia_thue'],errors="coerce")
# Bài tập 2: Xử lý giá trị khuyết thiếu (Missing Values Handling)
# Sau bước 1, bảng dữ liệu của bạn đang có một số giá trị NaN và NaT. 
# Hãy xử lý chúng theo các quy tắc nghiệp vụ sau:
# Cột so_dien_tieu_thu: 
# Điền các giá trị khuyết thiếu bằng mức tiêu thụ điện trung bình của toàn bộ các phòng.

# Cột gia_thue: 
# Điền giá trị khuyết thiếu bằng mức giá thuê trung bình tương ứng của từng loai_phong 
# (ví dụ: phòng VIP bị thiếu giá thì lấy trung bình giá của các phòng VIP khác lấp vào).

# # Cột ngay_thue: 
# Xóa hoàn toàn các dòng dữ liệu mà ngay_thue bị lỗi (tức là giá trị NaT), 
# vì không thể quản lý hợp đồng nếu không có ngày bắt đầu.
df_phongtro['so_dien_tieu_thu'] = df_phongtro['so_dien_tieu_thu'].fillna(df_phongtro['so_dien_tieu_thu'].mean())
df_phongtro['gia_thue'] = df_phongtro['gia_thue'].fillna(
    df_phongtro.groupby('loai_phong')['gia_thue'].transform('mean')
)
df_phongtro = df_phongtro.dropna(subset = ['ngay_thue'])
df_phongtro['tien_dien'] = df_phongtro['so_dien_tieu_thu'] * 3500
df_phongtro['tong_tien'] = df_phongtro['gia_thue'] + df_phongtro['tien_dien']
df_phongtro['nam_thue'] = df_phongtro['ngay_thue'].dt.year
df_phongtro['thang_thue'] = df_phongtro['ngay_thue'].dt.month
df_phongtro['loai_phong_clean'] = df_phongtro['loai_phong'].astype(str).str.strip()
tong_tien = df_phongtro.groupby('loai_phong_clean')['tong_tien'].sum()
so_phong_2013 = len(df_phongtro[df_phongtro['nam_thue']==2023])
ma_phong_tieu_dien = df_phongtro.loc[df_phongtro['so_dien_tieu_thu'].idxmax()]
print(ma_phong_tieu_dien)
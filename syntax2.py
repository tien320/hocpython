# Kiểm tra tổng quan cấu trúc, kích thước, bộ nhớ
df.info(memory_usage='deep')
df.shape              # (rows, columns)
df.dtypes             # Kiểu dữ liệu từng cột

# Thống kê nhanh các chỉ số định lượng
df.describe(percentiles=[0.01, 0.25, 0.5, 0.75, 0.99])

# Kiểm tra phân phối giá trị phân loại
df['status'].value_counts(dropna=False, normalize=True) * 100

# Kiểm tra số lượng giá trị duy nhất
df.nunique()
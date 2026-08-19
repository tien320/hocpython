# Ép kiểu dữ liệu
df['order_id'] = df['order_id'].astype(str)
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

# Tối ưu RAM cho cột Categorical (Dùng khi số lượng distinct < 50%)
df['status'] = df['status'].astype('category')

# Downcasting số để giảm tải bộ nhớ
df['amount'] = pd.to_numeric(df['amount'], downcast='float')
df['age'] = pd.to_numeric(df['age'], downcast='unsigned')
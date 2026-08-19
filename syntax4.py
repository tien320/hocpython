# Thống kê tỷ lệ null
null_pct = (df.isna().sum() / len(df)) * 100

# Xóa null theo điều kiện
df.dropna(subset=['order_id', 'user_id'], inplace=True)  # Xóa dòng nếu cột khóa bị null
df.dropna(axis=1, thresh=len(df) * 0.7)                 # Xóa cột nếu null > 30%

# Điền giá trị (Imputation)
df['amount'] = df['amount'].fillna(0)
df['category'] = df['category'].fillna('UNKNOWN')
df['price'] = df.groupby('category')['price'].transform(lambda x: x.fillna(x.median()))
# Giữ lại bản ghi mới nhất theo partition
df_dedup = df.sort_values('updated_at').drop_duplicates(
    subset=['order_id'], 
    keep='last'
)

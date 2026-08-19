# Lọc đa điều kiện (&: AND, |: OR, ~: NOT)
filtered = df[(df['age'] >= 18) & (df['city'].isin(['Hanoi', 'Danang'])) & (df['is_active'] == True)]

# Lọc dùng .query() (cú pháp ngắn gọn, dễ bảo trì)
threshold = 1000
filtered = df.query('age >= 18 and city in ["Hanoi", "Danang"] and amount > @threshold')

# Lọc với chuỗi và Regex
email_valid = df[df['email'].str.contains(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', na=False)]
# .loc (Truy cập theo Label / Điều kiện)
df.loc[df['amount'] > 500, ['order_id', 'user_id', 'amount']]

# .iloc (Truy cập theo vị trí số nguyên)
df.iloc[0:10, [0, 2, 4]]
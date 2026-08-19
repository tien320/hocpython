import numpy as np

# Nhiều điều kiện phức tạp (np.select)
conditions = [
    (df['score'] >= 90) & (df['vip'] == True),
    (df['score'] >= 75),
    (df['score'] >= 50)
]
choices = ['Diamond', 'Gold', 'Silver']
df['tier'] = np.select(conditions, choices, default='Bronze')

# Hai nhánh đơn giản (np.where)
df['is_high_value'] = np.where(df['amount'] > 1000, 1, 0)
df['year'] = df['created_at'].dt.year
df['month'] = df['created_at'].dt.to_period('M')
df['day_of_week'] = df['created_at'].dt.day_name()
df['is_weekend'] = df['created_at'].dt.dayofweek.isin([5, 6])
df['name'] = df['name'].str.strip().str.title()
df['domain'] = df['email'].str.split('@').str[1]
df['phone_clean'] = df['phone'].str.replace(r'[^0-9]', '', regex=True)
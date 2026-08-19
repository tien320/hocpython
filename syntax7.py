# Aggregation chuẩn (Named Aggregation)
summary = df.groupby(['store_id', 'category']).agg(
    total_sales=('amount', 'sum'),
    avg_price=('price', 'mean'),
    unique_buyers=('user_id', 'nunique'),
    max_transaction=('amount', 'max')
).reset_index()
# 1. Running Total (Tổng lũy kế - SUM() OVER(PARTITION BY ... ORDER BY ...))
df['cumulative_sales'] = df.groupby('user_id')['amount'].cumsum()

# 2. Ranking (ROW_NUMBER() / DENSE_RANK())
df['order_rank'] = df.groupby('user_id')['created_at'].rank(method='first', ascending=True)
df['dense_rank'] = df.groupby('category')['amount'].rank(method='dense', ascending=False)

# 3. Lag / Lead (SHIFT)
df['prev_order_amount'] = df.groupby('user_id')['amount'].shift(1)  # LAG(amount, 1)
df['next_order_amount'] = df.groupby('user_id')['amount'].shift(-1) # LEAD(amount, 1)

# 4. Moving Average (MA / Rolling Window)
df['rolling_7d_avg'] = (
    df.set_index('created_at')
      .groupby('store_id')['amount']
      .rolling('7D')
      .mean()
      .reset_index(level=0, drop=True)
)

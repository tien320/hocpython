import pandas as pd
import numpy as np

# Đọc dữ liệu từ nhiều nguồn khác nhau
df = pd.read_csv('data.csv', parse_dates=['created_at'])
df = pd.read_parquet('data.parquet')
df = pd.read_sql('SELECT * FROM orders WHERE status = "COMPLETED"', con=engine)

# Xuất dữ liệu (tối ưu nén khi làm ETL)
df.to_parquet('output.parquet', compression='snappy', index=False)
df.to_csv('output.csv', index=False)
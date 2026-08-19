# Pandas Cheatsheet & Cẩm Nang Cú Pháp Cho Data Engineering (DE) / ETL

Tài liệu này tổng hợp toàn bộ các cú pháp (syntax) thực chiến, phân nhóm logic theo quy trình xử lý dữ liệu chuẩn từ **Ingestion -> Profiling -> Cleaning -> Transformation -> Aggregation -> Storage & Optimization**.

---

## 📑 Mục Lục

1. [I/O & Batch Processing (Đọc & Ghi Dữ Liệu)](#1-io--batch-processing)
2. [Data Exploration & Schema Inspection (Khám Phá & Kiểm Tra)](#2-data-exploration--schema-inspection)
3. [Filtering, Slicing & Subsetting (Lọc & Truy Vấn)](#3-filtering-slicing--subsetting)
4. [Data Cleaning & Missing Values (Làm Sạch Dữ Liệu)](#4-data-cleaning--missing-values)
5. [Data Type Casting & Optimization (Ép Kiểu & Tối Ưu RAM)](#5-data-type-casting--optimization)
6. [Feature Engineering & Transformations (Biến Đổi Cột)](#6-feature-engineering--transformations)
7. [Aggregation, GroupBy & Window Functions (Tổng Hợp & Phân Tích)](#7-aggregation-groupby--window-functions)
8. [Joins, Merges & Concatenations (Kết Hợp Dữ Liệu)](#8-joins-merges--concatenations)
9. [Reshaping: Pivot, Melt & Stacking (Xoay & Chuyển Đổi Chiều)](#9-reshaping-pivot-melt--stacking)
10. [Production Best Practices & Anti-Patterns (Hiệu Năng & Quy Chuẩn)](#10-production-best-practices--anti-patterns)

---

## 1. I/O & Batch Processing

### 1.1. Đọc dữ liệu (Ingestion)

```python
import pandas as pd

# Đọc CSV với chỉ định kiểu dữ liệu và cột ngày tháng
df_csv = pd.read_csv(
    'data/source.csv',
    usecols=['order_id', 'user_id', 'amount', 'created_at'],
    dtype={'order_id': 'str', 'user_id': 'int64', 'amount': 'float32'},
    parse_dates=['created_at'],
    na_values=['NA', 'null', '']
)

# Đọc Parquet (định dạng tối ưu cho DE/Lakehouse)
df_parquet = pd.read_parquet('data/source.parquet', columns=['order_id', 'amount'])

# Đọc từ Database qua SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@host:5432/dbname')
df_sql = pd.read_sql('SELECT id, name, created_at FROM users WHERE status = :status',
                     con=engine, params={'status': 'ACTIVE'})

# Đọc file dung lượng lớn theo từng batch (Chunking)
chunk_size = 100_000
for chunk in pd.read_csv('huge_file.csv', chunksize=chunk_size):
    # Xử lý từng batch
    process_chunk(chunk)
```

### 1.2. Xuất dữ liệu (Storage & Export)

```python
# Xuất Parquet chuẩn nén (Khuyên dùng Snappy / ZSTD)
df.to_parquet('output/data.parquet', compression='snappy', index=False)

# Xuất CSV chuẩn ETL (không kèm index)
df.to_csv('output/data.csv', index=False, encoding='utf-8')

# Ghi trực tiếp vào Database (Bulk Insert)
df.to_sql('target_table', con=engine, if_exists='append', index=False, method='multi', chunksize=5000)
```

---

## 2. Data Exploration & Schema Inspection

```python
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
```

---

## 3. Filtering, Slicing & Subsetting

### 3.1. Boolean Masking & Query

```python
# Lọc đa điều kiện (&: AND, |: OR, ~: NOT)
filtered = df[(df['age'] >= 18) & (df['city'].isin(['Hanoi', 'Danang'])) & (df['is_active'] == True)]

# Lọc dùng .query() (cú pháp ngắn gọn, dễ bảo trì)
threshold = 1000
filtered = df.query('age >= 18 and city in ["Hanoi", "Danang"] and amount > @threshold')

# Lọc với chuỗi và Regex
email_valid = df[df['email'].str.contains(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', na=False)]
```

### 3.2. Slicing bằng `.loc` và `.iloc`

```python
# .loc (Truy cập theo Label / Điều kiện)
df.loc[df['amount'] > 500, ['order_id', 'user_id', 'amount']]

# .iloc (Truy cập theo vị trí số nguyên)
df.iloc[0:10, [0, 2, 4]]
```

---

## 4. Data Cleaning & Missing Values

### 4.1. Xử lý Missing Data

```python
# Thống kê tỷ lệ null
null_pct = (df.isna().sum() / len(df)) * 100

# Xóa null theo điều kiện
df.dropna(subset=['order_id', 'user_id'], inplace=True)  # Xóa dòng nếu cột khóa bị null
df.dropna(axis=1, thresh=len(df) * 0.7)                 # Xóa cột nếu null > 30%

# Điền giá trị (Imputation)
df['amount'] = df['amount'].fillna(0)
df['category'] = df['category'].fillna('UNKNOWN')
df['price'] = df.groupby('category')['price'].transform(lambda x: x.fillna(x.median()))
```

### 4.2. Xử lý Trùng lặp (Deduplication)

```python
# Giữ lại bản ghi mới nhất theo partition
df_dedup = df.sort_values('updated_at').drop_duplicates(
    subset=['order_id'],
    keep='last'
)
```

---

## 5. Data Type Casting & Optimization

```python
# Ép kiểu dữ liệu
df['order_id'] = df['order_id'].astype(str)
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

# Tối ưu RAM cho cột Categorical (Dùng khi số lượng distinct < 50%)
df['status'] = df['status'].astype('category')

# Downcasting số để giảm tải bộ nhớ
df['amount'] = pd.to_numeric(df['amount'], downcast='float')
df['age'] = pd.to_numeric(df['age'], downcast='unsigned')
```

---

## 6. Feature Engineering & Transformations

### 6.1. Conditional Logic (Tương đương `CASE WHEN`)

```python
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
```

### 6.2. Thao tác Ngày Tháng (Datetime Manipulation)

```python
df['year'] = df['created_at'].dt.year
df['month'] = df['created_at'].dt.to_period('M')
df['day_of_week'] = df['created_at'].dt.day_name()
df['is_weekend'] = df['created_at'].dt.dayofweek.isin([5, 6])
```

### 6.3. Chuỗi (String Vectorization)

```python
df['name'] = df['name'].str.strip().str.title()
df['domain'] = df['email'].str.split('@').str[1]
df['phone_clean'] = df['phone'].str.replace(r'[^0-9]', '', regex=True)
```

---

## 7. Aggregation, GroupBy & Window Functions

### 7.1. GroupBy & Multi-Aggregation

```python
# Aggregation chuẩn (Named Aggregation)
summary = df.groupby(['store_id', 'category']).agg(
    total_sales=('amount', 'sum'),
    avg_price=('price', 'mean'),
    unique_buyers=('user_id', 'nunique'),
    max_transaction=('amount', 'max')
).reset_index()
```

### 7.2. Window Functions (Tương đương SQL `OVER(PARTITION BY ... ORDER BY ...)`)

```python
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
```

---

## 8. Joins, Merges & Concatenations

### 8.1. Merge (SQL JOIN)

```python
# Left Join kết hợp 2 bảng
merged = pd.merge(
    orders,
    users,
    left_on='user_id',
    right_on='id',
    how='left',       # 'inner', 'left', 'right', 'outer', 'cross'
    suffixes=('_order', '_user'),
    indicator=True    # Tạo cột '_merge' ('left_only', 'both', 'right_only') để debug
)
```

### 8.2. Concat (SQL UNION ALL / Append)

```python
# UNION ALL nhiều bảng theo chiều dọc
df_full_year = pd.concat([df_q1, df_q2, df_q3, df_q4], axis=0, ignore_index=True)

# Ghép theo chiều ngang (Side-by-side)
df_features = pd.concat([df_numerical, df_categorical], axis=1)
```

---

## 9. Reshaping: Pivot, Melt & Stacking

### 9.1. Melt (Wide -> Long / Unpivot)

```python
# Chuyển các cột doanh thu tháng thành dòng
long_df = pd.melt(
    df,
    id_vars=['store_id', 'product_id'],
    value_vars=['jan_sales', 'feb_sales', 'mar_sales'],
    var_name='month',
    value_name='sales_amount'
)
```

### 9.2. Pivot Table (Long -> Wide)

```python
# Tạo ma trận báo cáo
pivot_df = pd.pivot_table(
    df,
    values='amount',
    index='store_id',
    columns='category',
    aggfunc='sum',
    fill_value=0
).reset_index()
```

---

## 10. Production Best Practices & Anti-Patterns

| Thao Tác                          | ❌ Anti-Pattern (Nên Tránh)                           | ✅ Best Practice (Nên Dùng)                                        | Lý Do                                               |
| :-------------------------------- | :---------------------------------------------------- | :----------------------------------------------------------------- | :-------------------------------------------------- |
| **Duyệt qua từng dòng**           | `for idx, row in df.iterrows():`                      | Dùng Vectorization: `df['c'] = df['a'] + df['b']` hoặc `np.select` | Nhanh hơn 50x - 500x nhờ code C bên dưới.           |
| **Gán cột cảnh báo**              | `df[df['a'] > 0]['b'] = 1` _(SettingWithCopyWarning)_ | `df.loc[df['a'] > 0, 'b'] = 1`                                     | Đảm bảo gán trực tiếp vào bộ nhớ DataFrame.         |
| **Thêm từng dòng vào DataFrame**  | `df = df.append(new_row)`                             | Gom vào `list` rồi `pd.concat([df, pd.DataFrame(rows)])`           | Tránh việc copy lại toàn bộ DataFrame mỗi lần chèn. |
| **Chuỗi xử lý (Method Chaining)** | Viết các biến trung gian rải rác                      | Dùng `(df.query(...).assign(...).groupby(...))`                    | Dễ đọc, dễ viết unit test, code chuẩn declarative.  |
| **Bộ nhớ (Memory)**               | Giữ nguyên kiểu `int64`, `float64` mặc định           | Chuyển sang `category`, `int32`, `float32`                         | Giảm 60-80% dung lượng RAM sử dụng.                 |

---

_Tài liệu tổng hợp phục vụ chuẩn hóa quy trình ETL & Data Pipeline._

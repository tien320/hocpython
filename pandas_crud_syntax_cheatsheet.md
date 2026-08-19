# Cẩm Nang Cú Pháp CRUD Trong Pandas

Tài liệu này tổng hợp toàn bộ các thao tác **CRUD (Create - Read - Update - Delete)** trên DataFrame và Series của Pandas, được chuẩn hóa theo phong cách code tối ưu (Vectorized, Production-ready).

---

## 📑 Mục Lục
1. [CREATE (Thêm Mới / Khởi Tạo)](#1-create-thêm-mới--khởi-tạo)
2. [READ (Đọc, Truy Vấn & Slicing)](#2-read-đọc-truy-vấn--slicing)
3. [UPDATE (Cập Nhật & Biến Đổi Dữ Liệu)](#3-update-cập-nhật--biến-đổi-dữ-liệu)
4. [DELETE (Xóa Dòng, Cột & Làm Sạch)](#4-delete-xóa-dòng-cột--làm-sạch)
5. [Bảng Đối Chiếu SQL CRUD vs Pandas CRUD](#5-bảng-đối-chiếu-sql-crud-vs-pandas-crud)

---

## 1. CREATE (Thêm Mới / Khởi Tạo)

### 1.1. Tạo DataFrame / Series Mới
```python
import pandas as pd
import numpy as np

# Tạo DataFrame từ Dictionary
df = pd.DataFrame({
    'user_id': [101, 102, 103],
    'username': ['alice', 'bob', 'charlie'],
    'balance': [150.0, 200.5, 50.0],
    'status': ['ACTIVE', 'PENDING', 'ACTIVE']
})

# Tạo DataFrame từ danh sách các Dictionary (dạng JSON records)
records = [{'user_id': 104, 'username': 'david', 'balance': 300.0, 'status': 'ACTIVE'}]
df_from_records = pd.DataFrame(records)
```

### 1.2. Thêm Cột Mới (Add Columns)
```python
# 1. Thêm cột với giá trị hằng số
df['country'] = 'VN'

# 2. Thêm cột dựa trên phép tính toán học (Vectorization)
df['balance_after_fee'] = df['balance'] * 0.95

# 3. Thêm cột bằng .assign() (hỗ trợ Method Chaining)
df = df.assign(
    tax=lambda x: x['balance'] * 0.1,
    is_vip=lambda x: x['balance'] >= 200
)

# 4. Thêm cột tại một vị trí cụ thể (index)
df.insert(loc=1, column='email', value=['a@test.com', 'b@test.com', 'c@test.com'])
```

### 1.3. Thêm Hàng Mới (Append / Insert Rows)
```python
# Tạo DataFrame hàng mới cần chèn
new_row = pd.DataFrame([{
    'user_id': 105, 
    'username': 'emma', 
    'balance': 500.0, 
    'status': 'ACTIVE'
}])

# Nối hàng mới vào DataFrame hiện tại
df = pd.concat([df, new_row], ignore_index=True)
```

---

## 2. READ (Đọc, Truy Vấn & Slicing)

### 2.1. Đọc Từ Nguồn Ngoài (Ingestion)
```python
# Đọc từ file/Database
df = pd.read_csv('users.csv')
df = pd.read_parquet('users.parquet')
df = pd.read_sql('SELECT * FROM users', con=engine)
```

### 2.2. Kiểm Tra & Khám Phá Nhanh (Inspection)
```python
df.head(5)       # 5 dòng đầu
df.tail(5)       # 5 dòng cuối
df.sample(3)     # Lấy ngẫu nhiên 3 dòng
df.shape         # Kích thước (dòng, cột)
df.info()        # Chi tiết kiểu dữ liệu & non-null
```

### 2.3. Lọc & Truy Vấn Hàng (Filter & Query)
```python
# 1. Boolean Masking (Lọc đa điều kiện)
active_rich = df[(df['status'] == 'ACTIVE') & (df['balance'] >= 100)]

# 2. Dùng .query() (ngắn gọn, trực quan)
min_balance = 100
filtered = df.query('status == "ACTIVE" and balance >= @min_balance')

# 3. Lọc theo danh sách (IN trong SQL)
selected_users = df[df['username'].isin(['alice', 'david'])]

# 4. Lọc theo chuỗi & Regex
gmail_users = df[df['email'].str.endswith('@gmail.com', na=False)]
```

### 2.4. Trích Xuất Dữ Liệu Theo Vị Trí / Nhãn (.loc & .iloc)
```python
# .loc: Dựa trên Label cột và Điều kiện dòng
df.loc[df['balance'] > 150, ['username', 'balance']]

# .iloc: Dựa trên chỉ số index nguyên thủy (Row 0 đến 2, Column 0 và 1)
df.iloc[0:3, [0, 1]]
```

---

## 3. UPDATE (Cập Nhật & Biến Đổi Dữ Liệu)

### 3.1. Cập Nhật Giá Trị Theo Điều Kiện (.loc)
```python
# Cập nhật 1 giá trị hoặc 1 cột cho các dòng thỏa mãn điều kiện
df.loc[df['username'] == 'alice', 'balance'] = 250.0

# Cập nhật nhiều cột đồng thời
df.loc[df['user_id'] == 102, ['status', 'balance']] = ['ACTIVE', 500.0]
```

### 3.2. Cập Nhật Phân Nhánh (CASE WHEN / IF-ELSE)
```python
# 1. Hai nhánh đơn giản (np.where)
df['risk_level'] = np.where(df['balance'] < 100, 'HIGH', 'LOW')

# 2. Nhiều nhánh phức tạp (np.select)
conditions = [
    df['balance'] >= 300,
    df['balance'] >= 100,
    df['balance'] < 100
]
choices = ['TIER_1', 'TIER_2', 'TIER_3']
df['tier'] = np.select(conditions, choices, default='UNKNOWN')
```

### 3.3. Thay Thế Trực Tiếp & Ánh Xạ (Replace & Map)
```python
# Thay thế giá trị cụ thể
df['status'] = df['status'].replace({'PENDING': 'IN_PROGRESS'})

# Map toàn bộ cột theo Dictionary (các giá trị không match thành NaN)
status_codes = {'ACTIVE': 1, 'IN_PROGRESS': 0, 'BANNED': -1}
df['status_code'] = df['status'].map(status_codes)
```

### 3.4. Xử Lý Missing Values (Imputation / Fillna)
```python
# Điền giá trị mặc định cho cột null
df['balance'] = df['balance'].fillna(0.0)

# Điền bằng giá trị trung bình/trung vị của nhóm
df['balance'] = df.groupby('status')['balance'].transform(lambda x: x.fillna(x.median()))
```

### 3.5. Đổi Tên Cột / Index (Rename)
```python
# Đổi tên cột
df = df.rename(columns={'username': 'user_name', 'balance': 'account_balance'})
```

---

## 4. DELETE (Xóa Dòng, Cột & Làm Sạch)

### 4.1. Xóa Cột (Drop Columns)
```python
# Xóa một hoặc nhiều cột
df = df.drop(columns=['country', 'balance_after_fee'])

# Xóa cột trực tiếp inplace (tiết kiệm bộ nhớ)
df.drop(columns=['email'], inplace=True, errors='ignore')
```

### 4.2. Xóa Dòng Theo Điều Kiện / Index (Drop Rows)
```python
# 1. Xóa dòng thông qua việc lọc giữ lại các dòng cần thiết
df = df[df['status'] != 'BANNED']

# 2. Xóa dòng theo chỉ số index
df = df.drop(index=[0, 2])
```

### 4.3. Xóa Dòng Trùng Lặp (Deduplication)
```python
# Xóa các dòng trùng lặp hoàn toàn
df = df.drop_duplicates()

# Xóa trùng theo cột khóa chính (giữ bản ghi cuối cùng)
df = df.drop_duplicates(subset=['user_id'], keep='last')
```

### 4.4. Xóa Dòng Chứa Null (Drop NA)
```python
# Xóa dòng nếu bất kỳ cột nào bị Null
df = df.dropna()

# Xóa dòng nếu các cột khóa chính bị Null
df = df.dropna(subset=['user_id', 'status'])

# Xóa cột nếu tỷ lệ Null vượt quá ngưỡng
df = df.dropna(axis=1, thresh=len(df) * 0.8)
```

---

## 5. Bảng Đối Chiếu SQL CRUD vs Pandas CRUD

| Hành Động | SQL Syntax (Database) | Pandas Syntax (DataFrame) |
| :--- | :--- | :--- |
| **CREATE (Row)** | `INSERT INTO table VALUES (...)` | `pd.concat([df, new_rows_df], ignore_index=True)` |
| **CREATE (Col)** | `ALTER TABLE ADD COLUMN col ...` | `df['new_col'] = value` hoặc `df.assign(...)` |
| **READ (All)** | `SELECT * FROM table` | `df` / `df.copy()` |
| **READ (Filter)** | `SELECT * WHERE col > 10` | `df[df['col'] > 10]` hoặc `df.query('col > 10')` |
| **READ (Cols)** | `SELECT col1, col2 FROM table` | `df[['col1', 'col2']]` hoặc `df.loc[:, ['col1', 'col2']]` |
| **UPDATE (Set)** | `UPDATE table SET col = val WHERE id = 1` | `df.loc[df['id'] == 1, 'col'] = val` |
| **UPDATE (Case)**| `CASE WHEN cond THEN a ELSE b END` | `np.where(cond, a, b)` / `np.select(...)` |
| **DELETE (Row)** | `DELETE FROM table WHERE status = 'X'` | `df = df[df['status'] != 'X']` |
| **DELETE (Col)** | `ALTER TABLE DROP COLUMN col` | `df = df.drop(columns=['col'])` |
| **DELETE (Dedup)**| `SELECT DISTINCT *` / `ROW_NUMBER()` | `df.drop_duplicates(subset=['id'], keep='last')` |

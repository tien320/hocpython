**Reading Data** (Đọc/Nạp dữ liệu) là bước khởi đầu bắt buộc trong mọi quy trình Data Engineering hay Data Analysis sử dụng Pandas. Mục tiêu của bước này là biến đổi các tập tin dữ liệu thô (Raw Data) ở nhiều định dạng khác nhau thành cấu trúc **DataFrame** chuẩn trong bộ nhớ RAM để tiến hành làm sạch, biến đổi và phân tích.

---

## 1. Cú pháp tổng quát & Bản chất

Hầu hết các hàm đọc dữ liệu trong Pandas đều tuân theo chuẩn đặt tên: `pd.read_<format>()`.

Khi thực thi, hàm này sẽ:

1. Mở file hoặc kết nối tới nguồn dữ liệu.
2. Phân tích cấu trúc (Parse) nội dung theo định dạng tương ứng.
3. Ép kiểu dữ liệu (Type Inference) cho từng cột.
4. Trả về một đối tượng **`pandas.DataFrame`**.

```
[Nguồn dữ liệu thô]  ──( pd.read_* )──>  [Pandas DataFrame (RAM)]
(CSV, Parquet, SQL...)

```

---

## 2. Các hàm đọc dữ liệu phổ biến & Trường hợp sử dụng

| Định dạng File | Hàm Pandas          | Lĩnh vực/Trường hợp dùng phổ biến                                                                     |
| -------------- | ------------------- | ----------------------------------------------------------------------------------------------------- |
| **CSV / Text** | `pd.read_csv()`     | Dữ liệu dạng bảng đơn giản, trao đổi giữa các hệ thống, file nhỏ đến trung bình.                      |
| **Excel**      | `pd.read_excel()`   | Báo cáo nghiệp vụ, dữ liệu kinh doanh, file có nhiều sheet (.xlsx).                                   |
| **JSON**       | `pd.read_json()`    | Dữ liệu log, phản hồi từ REST API, dữ liệu có cấu trúc lồng nhau (nested).                            |
| **Parquet**    | `pd.read_parquet()` | **Định dạng chuẩn trong Big Data / DE**. Nén tốt, lưu theo cột (columnar format), đọc/ghi siêu nhanh. |
| **SQL Query**  | `pd.read_sql()`     | Lấy dữ liệu trực tiếp từ các hệ quản trị CSDL (PostgreSQL, MySQL, SQL Server,...).                    |

---

## 3. Các tham số quan trọng cần nắm vững (Key Parameters)

Khi làm Data Engineering, dữ liệu thô hiếm khi "sạch". Bạn phải dùng các tham số của hàm `read_*()` để kiểm soát cách nạp dữ liệu:

### 3.1. Xử lý Header & Delimiter (Phân cách)

- **`sep` / `delimiter**`*(mặc định`,`)*: Ký tự phân cách các cột (ví dụ: `;`, `\t`cho file TSV,`|`).
- **`header`**: Xác định dòng nào chứa tên cột.
- `header=0`: Dòng đầu tiên là tên cột (mặc định).
- `header=None`: File không có dòng tiêu đề, Pandas sẽ tự gán tên cột là `0, 1, 2...`

### 3.2. Quản lý Kiểu dữ liệu & Bộ nhớ (Data Types & Memory)

- **`dtype`**: Ép kiểu dữ liệu cố định cho từng cột ngay khi nạp vào RAM. Giúp tối ưu bộ nhớ và tránh ép sai kiểu.
- _Ví dụ:_ `dtype={'user_id': str, 'price': float}` (giữ `user_id` dạng chuỗi để không mất số `0` ở đầu).

- **`parse_dates`**: Tự động chuyển đổi các cột chứa ngày tháng sang kiểu `datetime64`.
- _Ví dụ:_ `parse_dates=['created_at', 'updated_at']`.

### 3.3. Xử lý Ký tự & Mã hóa (Encoding & Formatting)

- **`encoding`**: Mã hóa ký tự của file thô. Mặc định là `'utf-8'`. Nếu gặp lỗi hiển thị tiếng Việt hoặc ký tự lạ, bạn thường phải chỉnh về `'utf-8-sig'`, `'latin1'`, hoặc `'cp1252'`.
- **`na_values`**: Định nghĩa danh sách các giá trị được coi là `NULL` / Missing data (ví dụ: `na_values=['N/A', 'NA', 'missing', '-']`).

### 3.4. Đọc dữ liệu lớn (Big Data / Chunking)

- **`usecols`**: Chỉ chọn đọc các cột cần thiết thay vì nạp toàn bộ file vào RAM (giảm tải memory rất nhiều).
- _Ví dụ:_ `usecols=['id', 'amount']`.

- **`chunksize`**: Trả về một iterator để đọc file theo từng khối (chunk) $N$ dòng. Rất hữu ích khi đọc file lớn hơn dung lượng RAM khả dụng.

---

## 4. Ví dụ tổng hợp trong Cụm công việc Data Engineering

```python
import pandas as pd

# 1. Đọc file CSV lỗi mã hóa, chứa ký tự phân cách ';', ép kiểu và lọc cột
df_csv = pd.read_csv(
    'sales_data.csv',
    sep=';',
    encoding='utf-8',
    usecols=['order_id', 'customer_id', 'amount', 'order_date'],
    dtype={'order_id': str, 'customer_id': str, 'amount': float},
    parse_dates=['order_date'],
    na_values=['UNKNOWN', 'NULL']
)

# 2. Đọc file Parquet (Tối ưu cho Data Lake)
df_parquet = pd.read_parquet('warehouse/fact_orders.parquet')

# 3. Đọc dữ liệu trực tiếp từ SQL Database via SQLAlchemy Engine
# df_sql = pd.read_sql("SELECT id, status FROM orders WHERE status = 'COMPLETED'", con=engine)

```

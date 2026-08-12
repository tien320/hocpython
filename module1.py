import io
import pandas as pd

# Dữ liệu giả lập 1: Bảng Giao dịch (phân cách bởi dấu '|')
transactions_csv = """tran_id|cust_id|tran_date|amount|channel
TX1001|C01|2026-08-10|500000|App
TX1002|C02|2026-08-11|INVALID|Web
TX1003|C01|2026-08-11|1200000|App
TX1004|C03|2026-08-12|750000|POS
TX1005|C04|2026-08-12|NULL|App"""

# Dữ liệu giả lập 2: Bảng Khách hàng
customers_csv = """cust_id,cust_name,join_date
C01,Nguyễn Văn A,2025-01-15
C02,Trần Thị B,2025-03-20
C03,Lê Văn C,2025-06-10
C04,Phạm Văn D,2026-02-01"""

df_trans = pd.read_csv(
    io.StringIO(transactions_csv),
    sep="|",
    usecols=[
        "tran_id",
        "cust_id",
        "tran_date",
        "amount",
        "channel"
    ],
    parse_dates= ["tran_date"],
    na_values=["INVALID","NULL"]
)
df_cus = pd.read_csv(io.StringIO(customers_csv), sep=',')
print(df_trans) # xem bảng
print(df_trans.dtypes) # xem kiểu dữ liệu
print(df_trans.shape) # số dòng số cột
print(df_trans.isna().sum()) # tổng số giá trị nan trong cột
print(df_trans.info()) # thông tin tổng quan 
#lưu s_amount là cột amount
s_amount = df_trans["amount"]
print(s_amount)
print(type(s_amount))
# lưu cột tran_id và amount vào 1 dataframe tên là df_sub
df_sub = df_trans[["tran_id","amount"]]
print(type(df_sub))
df_trans["amount"] = df_trans["amount"].astype(float)
print(df_trans.dtypes)


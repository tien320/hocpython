import io
import pandas as pd

# 1. Bảng Fact: Đơn hàng
orders_csv = """order_id,cust_id,product_id,amount
ORD101,C01,P01,1500000
ORD102,C02,P02,2300000
ORD103,C01,P01,800000
ORD104,C03,P03,450000"""

# 2. Bảng Dimension: Khách hàng
customers_csv = """cust_id,cust_name,city
C01,Nguyễn Văn A,Hà Nội
C02,Trần Thị B,Đà Nẵng
C04,Lê Văn D,TP.HCM"""

# 3. Bảng Log đơn hàng tháng 9 (Cùng cấu trúc với orders_csv)
sep_orders_csv = """order_id,cust_id,product_id,amount
ORD105,C02,P01,1200000
ORD106,C04,P03,3100000"""

df_orders = pd.read_csv(io.StringIO(orders_csv))
df_customers = pd.read_csv(io.StringIO(customers_csv))
df_sep_orders = pd.read_csv(io.StringIO(sep_orders_csv))

#Hãy thực hiện LEFT JOIN giữa bảng đơn hàng df_orders (bảng bên trái) và 
# bảng khách hàng df_customers (bảng bên phải) dựa trên 
# cột khóa cust_id.
#Lưu kết quả vào biến df_merged.
#Kiểm tra các đơn hàng không tìm thấy thông tin khách hàng 
# (bị mang giá trị NaN ở cột cust_name).
df_merged = pd.merge(df_orders,df_customers,on="cust_id",how="left")
print(df_merged)
missing = df_merged[df_merged["cust_name"].isna()]
print(missing)
#Hãy chồng bảng đơn hàng tháng 9 (df_sep_orders) xuống phía dưới bảng đơn hàng hiện tại (df_orders).
#Sử dụng pd.concat() với tham số ignore_index=True để đánh lại thứ tự chỉ số dòng.
#Lưu kết quả vào biến df_all_orders.
df_all_orders = pd.concat([df_orders,df_sep_orders],axis=0,ignore_index=True)
print(df_all_orders)
data_sales = {
    "city": ["Hà Nội", "Hà Nội", "TP.HCM", "TP.HCM"],
    "product_id": ["P01", "P02", "P01", "P02"],
    "revenue": [1000, 1500, 2000, 2500],
}
df_sales = pd.DataFrame(data_sales)
df_pivot = df_sales.pivot_table(
    index="city",columns="product_id",values="revenue",aggfunc="sum"
).reset_index()
print(df_pivot)
df_melted = pd.melt(
    df_pivot,
    id_vars="city",
    value_vars=["P01","P02"],
    var_name="product_id",
    value_name="revenue"
)
print(df_melted)
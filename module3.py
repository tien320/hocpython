import io
import pandas as pd

# Dữ liệu bảng Giao Dịch Bán Hàng
sales_csv = """order_id,cust_id,order_date,status,amount,region,category
ORD001,C01,2026-08-01,COMPLETED,1500000,North,Electronics
ORD002,C02,2026-08-01,COMPLETED,2300000,South,Fashion
ORD003,C01,2026-08-02,CANCELLED,800000,North,Electronics
ORD004,C03,2026-08-02,COMPLETED,450000,Central,Fashion
ORD005,C04,2026-08-03,COMPLETED,3100000,South,Electronics
ORD006,C02,2026-08-03,COMPLETED,1200000,Central,Electronics
ORD007,C01,2026-08-04,COMPLETED,2000000,North,Fashion
ORD008,C05,2026-08-04,PENDING,900000,South,Fashion"""

df_sales = pd.read_csv(io.StringIO(sales_csv), parse_dates=["order_date"])
#Lọc các đơn hàng có status == 'COMPLETED'.
#Gom nhóm theo khu vực (region).
#Tính tổng doanh thu (total_revenue) và tổng số đơn hàng (total_orders).
#Phẳng hóa dữ liệu bằng .reset_index().
df_report1 = (
    df_sales[df_sales["status"] == "COMPLETED"]
    .groupby("region")
    .agg(
        total_revenue = ("amount","sum"),
        total_orders = ("order_id","count")
    )
    .reset_index()
)
print(df_report1)
#Lọc các đơn hàng COMPLETED.
#Gom nhóm đồng thời theo 2 cột: region và category.
#Tính số lượng khách hàng duy nhất (unique_customers - dùng nunique) và giá trị đơn hàng trung bình (avg_amount - dùng mean).
#Trả về DataFrame dạng bảng phẳng.
df_report2 = (
    df_sales[df_sales["status"] == "COMPLETED"]
    .groupby(["region","category"])
    .agg(
        unique_customers = ("cust_id","nunique"),
        avg_amount = ("amount","mean")
    )
    .reset_index()
)
print(df_report2)
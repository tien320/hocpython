import io
import pandas as pd

# Dữ liệu bảng Đơn hàng (Orders)
orders_csv = """order_id,cust_id,order_date,status,amount,region
ORD101,C01,2026-08-01,COMPLETED,1500000,North
ORD102,C02,2026-08-02,PENDING,2300000,South
ORD103,C01,2026-08-03,COMPLETED,800000,North
ORD104,C03,2026-08-04,CANCELLED,450000,Central
ORD105,C04,2026-08-05,COMPLETED,3100000,South
ORD106,C02,2026-08-06,COMPLETED,1200000,Central"""

df_orders = pd.read_csv(io.StringIO(orders_csv), parse_dates=["order_date"])
# dùng iloc lấy 3 dòng đầu tiên và 2 cột cuối cùng
sub_iloc = df_orders.iloc[0:3,-2:] 
print(sub_iloc)
#sử dụng loc lọc ra amount và status của orderid ORD103
df_orders = df_orders.set_index("order_id")
ord103_info = df_orders.loc["ORD103",["amount","status"]]
print(ord103_info)
df_orders = df_orders.reset_index()
#lọc các giá trị cao >= 1000000 và status = completed
conditions = (df_orders["amount"] >= 1000000)&(df_orders["status"] == "COMPLETED")
cols = ["order_id","cust_id","amount"]
df_high_value = df_orders.loc[conditions,cols]
print(df_high_value)
# lọc điều kiện region = north south amount trong khoảng 1000000-3000000
cond_region = df_orders["region"].isin(["North","South"])
cond_amount = df_orders["amount"].between(1000000,3000000)
df_filtered = df_orders.loc[cond_region & cond_amount]
print(df_filtered)
# thêm cột priority gán các giá trị high cho đơn amount >2000000 các giá trị còn lại để NORMAL
df_orders["priority"] = "NORMAL"
df_orders.loc[df_orders["amount"] > 2000000, "priority"] = "HIGH"
print(df_orders[["order_id","amount","priority"]])
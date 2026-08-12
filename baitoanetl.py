import io
import pandas as pd

# ==============================================================================
# DỮ LIỆU ĐẦU VÀO THÔ (MÔ PHỎNG)
# ==============================================================================
raw_trans_csv = """tran_id;cust_id;tran_date;amount;status;channel
TX101;C01;2026-08-01;1500000;COMPLETED;App
TX102;C02;2026-08-01;2300000;COMPLETED;Web
TX103;C01;2026-08-02;ERR;COMPLETED;App
TX104;C03;2026-08-02;450000;CANCELLED;POS
TX105;C04;2026-08-03;3500000;COMPLETED;App
TX106;C02;2026-08-03;-100000;COMPLETED;Web"""

raw_sep_trans_csv = """tran_id;cust_id;tran_date;amount;status;channel
TX107;C01;2026-08-04;2000000;COMPLETED;App
TX108;C05;2026-08-04;1200000;COMPLETED;Web
TX109;C02;2026-08-05;800000;COMPLETED;POS"""

raw_cust_csv = """cust_id,cust_name,city
C01,Nguyễn Văn An,Hà Nội
C02,Trần Thị Bình,Đà Nẵng
C03,Lê Văn Cường,TP.HCM
C04,Phạm Minh Đạt,Hà Nội"""

df_trans = pd.read_csv(
    io.StringIO(raw_trans_csv),
    sep=';',
    usecols=[
        "tran_id",
        "cust_id",
        "tran_date",
        "amount",
        "status",
        "channel"
    ],
    parse_dates=["tran_date"],
    na_values= ["ERR","NULL"]
)
df_sep_trans = pd.read_csv(
    io.StringIO(raw_sep_trans_csv),
    sep=';',
    usecols=[
        "tran_id",
        "cust_id",
        "tran_date",
        "amount",
        "status",
        "channel"
    ],
    parse_dates=["tran_date"]
)
df_cust = pd.read_csv(
    io.StringIO(raw_cust_csv),
    sep = ',',
    usecols=[
        "cust_id",
        "cust_name",
        "city"
    ]
)
df_all_trans = pd.concat([df_trans,df_sep_trans],axis=0,ignore_index=True)
#Ép cột amount sang kiểu số thực (float).
#Lọc bỏ các dòng có status == 'CANCELLED' 
# hoặc giá trị amount bị NaN hoặc amount <= 0.
#Lọc lấy các đơn hàng diễn ra trong khu vực 
# channel thuộc danh sách ['App', 'Web'].
df_all_trans["amount"] = df_all_trans["amount"].astype(float)
cond_status = df_all_trans["status"] != "CANCELLED"
cond_amount = df_all_trans["amount"].notna()
cond_channel = df_all_trans["channel"].isin(["App","Web"])
df_clean = df_all_trans[cond_status & cond_amount & cond_channel]
#Gom nhóm dữ liệu theo từng cust_id và tính:
#total_spend: Tổng tiền khách hàng đã chi tiêu (sum).
#trans_count: Tổng số đơn hàng thành công (count).
#avg_spend: Số tiền trung bình trên mỗi đơn hàng (mean).
#Chỉ giữ lại những khách hàng có total_spend >= 1,000,000 (Tương đương điều kiện HAVING).
#Phẳng hóa dữ liệu với .reset_index().
df_report = (
    df_clean
    .groupby("cust_id")
    .agg(
        total_spend = ("amount","sum"),
        trans_count = ("tran_id","count"),
        avg_spend = ("amount","mean")
    )
    .query("total_spend >= 1000000")
    .reset_index()
)
print(df_report)
#Thực hiện LEFT JOIN bảng tổng hợp ở Bước 3 với
#  raw_customers.csv dựa theo cust_id.
#Điền giá trị mặc định cho những khách hàng bị khuyết tên/thành phố: 
# cust_name -> 'Khách Vãng Lai', city -> 'Chưa xác định'.
#Thêm một cột mới đặt tên customer_rank:
#Giá trị 'VIP' nếu total_spend >= 3,000,000.

#Giá trị 'MEMBER' cho các trường hợp còn lại.

#Xắp xép kết quả giảm dần theo total_spend.
df_final = pd.merge(df_report, df_cust, on="cust_id", how="left")
df_final["cust_name"] = df_final["cust_name"].fillna("Khách Vãng Lai")
df_final["city"] = df_final["city"].fillna("Chưa xác định")
df_final["customer_rank"] = "MEMBER"
df_final.loc[df_final["total_spend"]>=3000000,"customer_rank"] = "VIP"
df_final = df_final[
    ["cust_id",
    "cust_name",
    "city",
    "trans_count",
    "total_spend",
    "avg_spend",
    "customer_rank"
    ]
].sort_values(by="total_spend",ascending=False)
print(df_final.to_string(index=False))
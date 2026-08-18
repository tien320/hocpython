import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from prophet import Prophet

# ==========================================
# 1. KẾT NỐI VÀ LẤY DỮ LIỆU TỪ ORACLE
# ==========================================
print("[1/5] Đang tải dữ liệu từ Oracle...")
ORACLE_URI = "oracle+oracledb://OLIST:123456@localhost:1521/?service_name=XEPDB1"
engine = create_engine(ORACLE_URI)

# Truy vấn tổng doanh thu theo ngày từ bảng Fact
query = """
    SELECT "date", SUM(revenue) as total_revenue 
    FROM fact_outbound_daily 
    GROUP BY "date" 
    ORDER BY "date"
"""
df = pd.read_sql(query, engine)

# ==========================================
# 2. TIỀN XỬ LÝ DỮ LIỆU CHO PROPHET
# ==========================================
print("[2/5] Đang cấu trúc lại dữ liệu...")
# Nguyên tắc của thuật toán Prophet: 
# Yêu cầu cột thời gian tên là 'ds' và cột mục tiêu (cần dự báo) tên là 'y'
df = df.rename(columns={'date': 'ds', 'total_revenue': 'y'})
df['ds'] = pd.to_datetime(df['ds'])
df = df.dropna()

# ==========================================
# 3. HUẤN LUYỆN MÔ HÌNH (TRAIN MODEL)
# ==========================================
print("[3/5] Đang huấn luyện thuật toán Prophet (Machine Learning)...")
# interval_width=0.95: Đặt độ tin cậy của dự báo là 95%
model = Prophet(interval_width=0.95, daily_seasonality=False, yearly_seasonality=True)
model.fit(df)

# ==========================================
# 4. DỰ BÁO TƯƠNG LAI (FORECASTING)
# ==========================================
print("[4/5] Đang tính toán dự báo cho 30 ngày tới...")
# Yêu cầu mô hình tạo ra các mốc thời gian cho 30 ngày tiếp theo
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

print("\n=== KẾT QUẢ DỰ BÁO 5 NGÀY TỚI ===")
# yhat: Giá trị dự báo chính
# yhat_lower / yhat_upper: Khoảng sai số dưới/trên
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# ==========================================
# 5. TRỰC QUAN HÓA (VISUALIZATION)
# ==========================================
print("\n[5/5] Đang vẽ biểu đồ xu hướng...")
fig = model.plot(forecast)
plt.title("Dự báo xu hướng doanh thu Olist trong 30 ngày tới", fontsize=14)
plt.xlabel("Thời gian (Năm)", fontsize=12)
plt.ylabel("Doanh thu (BRL)", fontsize=12)

# Hiển thị biểu đồ
plt.show()
from sqlalchemy.types import Date, Numeric

# ==========================================
# 6. GHI KẾT QUẢ DỰ BÁO VÀO DATA WAREHOUSE (ORACLE)
# ==========================================
print("\n[6/6] Đang ghi kết quả dự báo ngược lại Oracle...")

def save_forecast_to_oracle(forecast_df, engine):
    # Trích xuất 4 cột quan trọng nhất từ kết quả của Prophet
    # ds: Ngày tháng
    # yhat: Doanh thu dự báo
    # yhat_lower, yhat_upper: Khoảng sai số (min/max)
    df_to_save = forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    
    # Đổi tên cột cho chuẩn mực Data Warehouse
    df_to_save = df_to_save.rename(columns={
        'ds': 'forecast_date',
        'yhat': 'predicted_revenue',
        'yhat_lower': 'revenue_lower_bound',
        'yhat_upper': 'revenue_upper_bound'
    })
    
    # Ép kiểu dữ liệu để Oracle hiểu chính xác (tránh lỗi Float binary precision)
    dtype_mapping = {
        'forecast_date': Date(),
        'predicted_revenue': Numeric(12, 2),
        'revenue_lower_bound': Numeric(12, 2),
        'revenue_upper_bound': Numeric(12, 2)
    }
    
    try:
        # Ghi dữ liệu tạo thành bảng mới fact_revenue_forecast
        df_to_save.to_sql(
            name='fact_revenue_forecast', 
            con=engine, 
            if_exists='replace', 
            index=False,
            dtype=dtype_mapping
        )
        print("  -> Bảng 'fact_revenue_forecast' đã được lưu thành công vào Oracle!")
    except Exception as e:
        print(f"  -> LỖI ORACLE: {e}")

# Gọi hàm thực thi
save_forecast_to_oracle(forecast, engine)
print("\n=== QUY TRÌNH DATA PIPELINE & MACHINE LEARNING HOÀN TẤT ===")
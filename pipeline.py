import pandas as pd
import os

# ==========================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==========================================
# Thay đổi đường dẫn này thành thư mục chứa các file CSV của bạn.
# Ví dụ trên Windows: 'C:/Users/Data/Olist/'
# Ví dụ nếu file code nằm cùng thư mục với CSV: './'
DATA_FOLDER = 'C:/Users/PC/OneDrive/Desktop/tien20235228/hocpython/olist_dataset'
def load_data(folder_path: str) -> tuple:
    """Đọc dữ liệu thô từ folder."""
    print("[1/4] Đang khởi tạo và đọc dữ liệu từ CSV...")
    
    # Hàm os.path.join giúp tự động ghép nối đường dẫn chuẩn xác trên mọi hệ điều hành
    orders_path = os.path.join(folder_path, 'olist_orders_dataset.csv')
    items_path = os.path.join(folder_path, 'olist_order_items_dataset.csv')
    products_path = os.path.join(folder_path, 'olist_products_dataset.csv')
    
    try:
        orders = pd.read_csv(orders_path)
        items = pd.read_csv(items_path)
        products = pd.read_csv(products_path)
        print("  -> Đọc file thành công!")
        return orders, items, products
    except FileNotFoundError as e:
        print(f"LỖI: Không tìm thấy file. Vui lòng kiểm tra lại tên file và đường dẫn FOLDER_PATH.\nChi tiết: {e}")
        exit()

def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch bảng Orders và chuẩn hóa thời gian."""
    print("[2/4] Đang làm sạch dữ liệu Orders...")
    df = orders[orders['order_status'] == 'delivered'].copy()
    df = df.dropna(subset=['order_delivered_customer_date'])
    
    # Chuyển đổi timestamp và trích xuất ngày
    time_cols = ['order_purchase_timestamp', 'order_delivered_customer_date']
    for col in time_cols:
        df[col] = pd.to_datetime(df[col])
        
    df['purchase_date'] = df['order_purchase_timestamp'].dt.date
    return df

def clean_and_merge_products(items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Xử lý giá trị rỗng và gộp thông tin sản phẩm vào chi tiết đơn hàng."""
    print("[3/4] Đang xử lý và hợp nhất dữ liệu Products & Items...")
    products['product_category_name'] = products['product_category_name'].fillna('unknown_category')
    return pd.merge(items, products, on='product_id', how='left')

def build_outbound_fact(orders_clean: pd.DataFrame, items_products: pd.DataFrame) -> pd.DataFrame:
    """Xây dựng Fact Table cho luồng Xuất kho (Sales Outbound)."""
    print("[4/4] Đang xây dựng Fact Table và tính toán tổng hợp...")
    fact_sales = pd.merge(orders_clean, items_products, on='order_id', how='inner')
    
    # Tính tổng lượng bán và doanh thu theo Ngày & Sản phẩm
    outbound_daily = fact_sales.groupby(['purchase_date', 'product_id']).agg(
        sales_volume=('order_item_id', 'count'),
        revenue=('price', 'sum')
    ).reset_index()
    
    outbound_daily = outbound_daily.rename(columns={'purchase_date': 'date'})
    # Sắp xếp theo ngày tăng dần
    outbound_daily = outbound_daily.sort_values(by='date')
    
    return outbound_daily

def main():
    """Hàm điều phối toàn bộ quy trình."""
    print("=== BẮT ĐẦU CHẠY PIPELINE ===")
    
    # Thực thi tuần tự các bước
    orders, items, products = load_data(DATA_FOLDER)
    orders_clean = clean_orders(orders)
    items_products = clean_and_merge_products(items, products)
    outbound_daily = build_outbound_fact(orders_clean, items_products)
    
    # Lưu kết quả ra một file CSV mới (Đã làm sạch)
    output_filename = 'fact_outbound_daily.csv'
    outbound_daily.to_csv(output_filename, index=False)
    
    print("=== PIPELINE HOÀN TẤT ===")
    print(f"File kết quả đã được lưu tại: {os.path.abspath(output_filename)}")
    print("\n[Preview 5 dòng đầu tiên của dữ liệu đã làm sạch]")
    print(outbound_daily.head())

if __name__ == "__main__":
    main()
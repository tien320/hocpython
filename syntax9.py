# Chuyển các cột doanh thu tháng thành dòng
long_df = pd.melt(
    df,
    id_vars=['store_id', 'product_id'],
    value_vars=['jan_sales', 'feb_sales', 'mar_sales'],
    var_name='month',
    value_name='sales_amount'
)
# Tạo ma trận báo cáo
pivot_df = pd.pivot_table(
    df,
    values='amount',
    index='store_id',
    columns='category',
    aggfunc='sum',
    fill_value=0
).reset_index()
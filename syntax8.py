# Left Join kết hợp 2 bảng
merged = pd.merge(
    orders,
    users,
    left_on='user_id',
    right_on='id',
    how='left',       # 'inner', 'left', 'right', 'outer', 'cross'
    suffixes=('_order', '_user'),
    indicator=True    # Tạo cột '_merge' ('left_only', 'both', 'right_only') để debug
)
# UNION ALL nhiều bảng theo chiều dọc
df_full_year = pd.concat([df_q1, df_q2, df_q3, df_q4], axis=0, ignore_index=True)

# Ghép theo chiều ngang (Side-by-side)
df_features = pd.concat([df_numerical, df_categorical], axis=1)
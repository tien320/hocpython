LAB 34 — Data Splitting & Cross-Validation
Sao chép

1. TRAIN / VALIDATION / TEST
   Tập Chức năng
   Train Học tham số \(w,b\)
   Validation Chọn C, class_weight, threshold
   Test Đánh giá cuối cùng

2. DATA LEAKAGE

- Không fit() preprocessing trên Validation/Test.
- Fit StandardScaler và SimpleImputer trên Train; chỉ transform() trên Validation/Test.
- Dùng Pipeline để tránh leakage trong Cross-Validation.

3. K-FOLD CROSS-VALIDATION

Chia dữ liệu phát triển thành \(K\) phần. Mỗi lượt dùng \(K-1\) phần để train, một phần để validation. Lặp \(K\) lần.
\[
CV*{mean}=\frac{1}{K}\sum*{i=1}^{K}Score_i
\]

\[
CV*{std}=\sqrt{\frac{1}{K}\sum*{i=1}^{K}(Score*i-CV*{mean})^2}
\]

- Mean: hiệu năng trung bình.
- Std: mức biến động giữa các Fold, không phải bảo đảm về hiệu năng tương lai.

4. STRATIFIED K-FOLD

Giữ tỷ lệ lớp 0/1 tương đối giống nhau giữa các Fold. Đặc biệt hữu ích cho Fraud Detection.

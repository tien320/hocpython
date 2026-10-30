Trong cơ sở dữ liệu quan hệ, **chuẩn hóa dữ liệu (Database Normalization)** là quá trình tổ chức các bảng và mối quan hệ để **giảm thiểu dư thừa dữ liệu (data redundancy)** và **loại bỏ các bất thường (anomalies)** khi thêm (Insert), sửa (Update), hoặc xóa (Delete).

Quá trình này tuân theo các cấp bậc gọi là **Dạng chuẩn (Normal Forms - NF)**, từ thấp lên cao (dạng sau phải thỏa mãn toàn bộ điều kiện của dạng trước).

---

### 1. Dạng chuẩn 1 (1NF - First Normal Form)

- **Quy tắc:** Mỗi ô dữ liệu chỉ chứa **giá trị nguyên tử (atomic value)** — nghĩa là một giá trị duy nhất, không chứa danh sách/mảng; không có các nhóm cột lặp lại.
- **Vi phạm 1NF:** Cột `PhoneNumbers` chứa chuỗi `"0912..., 0988..."` hoặc có các cột `Phone1`, `Phone2`, `Phone3`.
- **Cách khắc phục:** Tách thành các dòng riêng biệt hoặc tạo một bảng riêng cho số điện thoại gắn với khóa ngoại.

---

### 2. Dạng chuẩn 2 (2NF - Second Normal Form)

- **Quy tắc:** Đã đạt **1NF** VÀ **mọi thuộc tính không khóa phải phụ thuộc hàm đầy đủ vào toàn bộ khóa chính**, không được phụ thuộc vào một phần của khóa (chỉ áp dụng khi khóa chính là khóa phức hợp - Composite Key).
- **Vi phạm 2NF:** Bảng `OrderDetail(OrderID, ProductID, Quantity, ProductName)`. Khóa chính là `(OrderID, ProductID)`, nhưng `ProductName` chỉ phụ thuộc riêng vào `ProductID`.
- **Cách khắc phục:** Tách `ProductName` ra bảng `Products(ProductID, ProductName)` riêng.

---

### 3. Dạng chuẩn 3 (3NF - Third Normal Form)

- **Quy tắc:** Đã đạt **2NF** VÀ **không có phụ thuộc bắc cầu (transitive dependency)** — nghĩa là thuộc tính không khóa không được phụ thuộc vào một thuộc tính không khóa khác.
- **Vi phạm 3NF:** Bảng `Employees(EmpID, Name, DeptID, DeptName)`. Trong đó `EmpID -> DeptID`, và `DeptID -> DeptName`. Ở đây `DeptName` phụ thuộc bắc cầu vào `EmpID` qua `DeptID`.
- **Cách khắc phục:** Tách thành 2 bảng: `Employees(EmpID, Name, DeptID)` và `Departments(DeptID, DeptName)`.

---

### 4. Dạng chuẩn Boyce-Codd (BCNF - Boyce-Codd Normal Form)

- **Quy tắc:** Là phiên bản chặt chẽ hơn của 3NF. Với mọi phụ thuộc hàm có dạng $X \rightarrow Y$, thì **$X$ bắt buộc phải là một siêu khóa (Super Key)**.
- **Mục đích:** Xử lý các trường hợp đặc biệt khi bảng có nhiều khóa ứng viên chồng chéo (overlapping candidate keys) mà 3NF chưa bao quát hết.

---

### 5. Dạng chuẩn 4 (4NF) & Dạng chuẩn 5 (5NF)

- **4NF (Fourth Normal Form):** Đã đạt BCNF và **không chứa phụ thuộc đa trị (multi-valued dependencies)** độc lập trong cùng một bảng. _(Ví dụ: Một giảng viên có nhiều kỹ năng và dạy nhiều môn không liên quan nhau, nếu để chung một bảng sẽ sinh tích Descartes)_.
- **5NF (Fifth Normal Form / Project-Join NF):** Đảm bảo bảng không thể bị phân rã tiếp thành các bảng nhỏ hơn mà khi Join lại không tạo ra các dòng dữ liệu ảo (spurious tuples).

---

### Ứng dụng thực tế

- Trong hầu hết các dự án phần mềm và doanh nghiệp thực tế, hệ thống thường được thiết kế chuẩn hóa đến **3NF hoặc BCNF**. Đây là điểm cân bằng lý tưởng giữa tính toàn vẹn dữ liệu và độ phức tạp khi viết truy vấn.
- Trong các hệ thống phân tích dữ liệu, báo cáo (Data Warehouse / OLAP), người ta thường chủ động **phi chuẩn hóa (Denormalization)** về dạng Star Schema hoặc Snowflake Schema để giảm bớt số lượng phép `JOIN`, ưu tiên tốc độ đọc.

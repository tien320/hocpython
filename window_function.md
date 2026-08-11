Ngoài `DENSE_RANK()`, SQL hỗ trợ một hệ thống các hàm cửa sổ (Window Functions) rất phong phú. Chúng được chia thành **3 nhóm chính**:

---

### 1. Nhóm xếp hạng (Ranking Functions)

Dùng để đánh thứ tự, chia thứ hạng cho các dòng trong cùng một nhóm (`PARTITION BY`).

| Hàm                | Cách hoạt động                                                                                          | Ví dụ thực tế                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **`ROW_NUMBER()`** | Gán số thứ tự duy nhất $1, 2, 3...$ cho từng dòng (ngay cả khi trùng giá trị cũng không bị lặp lại số). | Lấy đúng 1 bài hát bán chạy nhất mỗi thể loại (không lấy đồng hạng).         |
| **`RANK()`**       | Xếp hạng có đồng hạng, nhưng **bị nhảy số** ở vị trí tiếp theo (1, 2, 2, 4).                            | Xếp hạng trao giải thể thao (2 huy chương bạc thì không có huy chương đồng). |
| **`NTILE(n)`**     | Chia các dòng trong nhóm thành `n` phần bằng nhau và đánh số thứ tự phân đoạn ($1, 2... n$).            | Chia bài hát thành 4 nhóm theo doanh thu (Top 25%, Top 50%,...).             |

---

### 2. Nhóm giá trị / Giá trị lệch (Value / Analytic Functions)

Dùng để truy cập dữ liệu của các dòng khác trong cùng tập kết quả mà **không cần `JOIN` lại bảng**.

| Hàm                    | Cách hoạt động                                      | Ví dụ thực tế                                                       |
| ---------------------- | --------------------------------------------------- | ------------------------------------------------------------------- |
| **`LAG(col, n)`**      | Lấy giá trị của cột ở dòng **phía trước** $n$ dòng. | So sánh doanh thu bài hát này với bài hát bán chạy liền trước nó.   |
| **`LEAD(col, n)`**     | Lấy giá trị của cột ở dòng **phía sau** $n$ dòng.   | So sánh doanh thu bài này với bài bán kém hơn liền sau.             |
| **`FIRST_VALUE(col)`** | Lấy giá trị đầu tiên trong nhóm cửa sổ.             | Lấy ra tên bài hát bán chạy nhất để hiển thị bên cạnh các bài khác. |
| **`LAST_VALUE(col)`**  | Lấy giá trị cuối cùng trong nhóm cửa sổ.            | Lấy giá trị của bài hát bán kém nhất trong thể loại.                |

---

### 3. Nhóm tổng hợp (Aggregate Window Functions)

Là các hàm tổng hợp quen thuộc (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) nhưng khi thêm mệnh đề `OVER(...)`, chúng không gom dòng lại mà giữ nguyên từng dòng và tính toán dồn tích (running total).

| Hàm                        | Cách hoạt động khi dùng làm Window Function                              | Ví dụ thực tế                                                                |
| -------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| **`SUM(col) OVER(...)`**   | Tính tổng dồn tích (Running Total) hoặc tổng của cả nhóm trên từng dòng. | Tính % đóng góp doanh thu của bài hát so với **tổng doanh thu cả thể loại**. |
| **`AVG(col) OVER(...)`**   | Tính giá trị trung bình trên từng dòng.                                  | So sánh giá bài hát này với **giá trung bình** của thể loại đó.              |
| **`COUNT(col) OVER(...)`** | Đếm số lượng dòng trong nhóm.                                            | Đếm xem thể loại này có tổng cộng bao nhiêu bài hát.                         |

---

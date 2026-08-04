# Phần CSDL MySQL

## Ngày 1

SELECT [Danh sách các cột]
FROM [Tên bảng]
WHERE [Điều kiện lọc dữ liệu];
Toán tử,Ý nghĩa,Ví dụ thực tế,Ghi chú
=,Bằng,WHERE Country = 'USA',Chuỗi ký tự phải để trong nháy đơn '...'
<> hoặc !=,Khác,WHERE Country <> 'USA',Lấy tất cả ngoại trừ 'USA'
">, <","Lớn hơn, Nhỏ hơn",WHERE Total > 10,"Dùng cho kiểu Số, Ngày tháng"
">=, <=",Lớn/Nhỏ hơn hoặc bằng,WHERE Total >= 15.00,Số thực dùng dấu chấm . phân cách
BETWEEN A AND B,"Trong khoảng [A, B]",WHERE Total BETWEEN 5 AND 10,Bao gồm cả 2 đầu (tương đương ≥5 và ≤10)
"IN (v1, v2, ...)",Thuộc một danh sách,"WHERE City IN ('Paris', 'London')",Tối ưu hơn việc viết nhiều lệnh OR 3. Các thao tác mở rộng & Quy tắc quan trọng
Ngoài các phép so sánh trên, bạn cần nắm thêm 3 thao tác bổ trợ rất quan trọng của Ngày 1:

A. Xử lý giá trị trống (NULL)
Trong CSDL, khi một ô không có dữ liệu, giá trị của nó là NULL (không phải là số 0 hay chuỗi rỗng '').

❌ Sai: WHERE Composer = NULL (Không dùng toán tử = với NULL).

✅ Đúng: WHERE Composer IS NULL (chưa có dữ liệu) hoặc WHERE Composer IS NOT NULL (đã có dữ liệu).
B. Lọc trùng lặp (DISTINCT)
Nhiều dòng có thể chứa giá trị giống nhau. Dùng DISTINCT ngay sau SELECT để chỉ lấy các giá trị duy nhất

SELECT DISTINCT Country FROM customer;

C. Quy tắc sử dụng dấu nháy và dấu chấm phẩy
Dấu nháy đơn ('...'): Dùng cho Chuỗi chữ ('Paris') và Ngày tháng ('2021-01-01').

Số (Số nguyên/Số thập phân): Viết trực tiếp, KHÔNG bọc dấu nháy (10, 0.99).

Dấu chấm phẩy (;): Bắt buộc đặt ở cuối mỗi câu lệnh SQL để báo hiệu kết thúc câu lệnh.

USE chinook;

-- 1. Lấy tất cả cột từ bảng track
SELECT \*
FROM track;

-- 2. Chỉ lấy các cột cần thiết + Dùng BETWEEN + Dùng phép khác (<>)
SELECT Name, Composer, UnitPrice, Milliseconds
FROM track
WHERE Milliseconds BETWEEN 180000 AND 240000 -- Dài từ 3 đến 4 phút
AND UnitPrice <> 0.99; -- Giá khác 0.99 USD

-- 3. Kiểm tra dữ liệu NULL + Toán tử IN
SELECT FirstName, LastName, Company, Country
FROM customer
WHERE Company IS NOT NULL -- Có thông tin công ty
AND Country IN ('USA', 'Canada', 'Brazil'); -- Thuộc khu vực Châu Mỹ

### Tổng Kết Ngày 1 SQL: Nền Tảng Truy Vấn Dữ Liệu SQL

Dưới đây là bức tranh toàn cảnh về những gì bạn đã làm chủ trong Ngày 1, giải đáp bản chất của các câu lệnh, lý do tồn tại và giá trị thực tế mà chúng mang lại.1. Các câu truy vấn Ngày 1 là gì?Ở Ngày 1, bạn đã học nhóm lệnh cơ bản nhất thuộc ngôn ngữ DQL (Data Query Language) — Ngôn ngữ truy vấn dữ liệu:$$\text{SQL Query} = \mathbf{SELECT} \text{ (Cột)} + \mathbf{FROM} \text{ (Bảng)} + \mathbf{WHERE} \text{ (Điều kiện)}$$SELECT: Chỉ định cụ thể các danh mục thông tin (cột) bạn muốn rút trích ra.FROM: Xác định chính xác "kho" hoặc "ngăn kéo" (bảng) chứa dữ liệu đó.WHERE: Bộ lọc dùng để nhặt ra đúng các bản ghi (dòng) thỏa mãn điều kiện.Tập toán tử so sánh (=, <>, >, <, BETWEEN, IN, IS NULL): Các công cụ logic giúp bạn định nghĩa điều kiện lọc chính xác đến từng con số, chuỗi ký tự hay trạng thái dữ liệu.2. Tại sao lại phải dùng các câu truy vấn này?Trong các hệ thống thực tế (như ứng dụng bán hàng, thương mại điện tử hay ngân hàng), cơ sở dữ liệu có thể chứa hàng triệu cho đến hàng tỷ dòng dữ liệu.Nếu không có SELECT & FROM: Bạn không thể giao tiếp với máy chủ cơ sở dữ liệu để bảo nó lấy thông tin ra.Nếu không có WHERE và bộ lọc: Máy tính sẽ buộc phải tải toàn bộ kho dữ liệu lên màn hình. Việc này gây tràn bộ nhớ (Out of Memory), làm sập hệ thống và bạn cũng không thể tự đọc hàng triệu dòng để tìm thông tin mình cần.
Yếu tố,Giá trị kỹ thuật,Giá trị thực tế / Kinh doanh
Tiết kiệm tài nguyên,"Chỉ lấy đúng các cột/dòng cần thiết, giảm tải cho mạng và RAM.","Hệ thống chạy mượt mà, phản hồi người dùng trong vài miligiây."
Chính xác & Khách quan,"Lọc dữ liệu theo logic toán tử (=, BETWEEN, IN) loại bỏ hoàn toàn sai sót do con người.","Đảm bảo tính chính xác cho các con số tài chính, hóa đơn, thông tin khách hàng."
Hỗ trợ ra quyết định,Rút trích nhanh các tập dữ liệu nhỏ theo tiêu chí cụ thể.,"Giúp doanh nghiệp trả lời ngay lập tức các câu hỏi như: ""Tìm danh sách hóa đơn trên 10 USD ở Châu Âu để gửi khuyến mãi""."

## NGÀY 2

Chào mừng bạn bước sang Ngày 2!

Hôm nay chúng ta sẽ trang bị thêm những công cụ mạnh mẽ để làm chủ việc lọc, tìm kiếm và sắp xếp dữ liệu. Sau Ngày 2, bạn có thể xử lý các bài toán truy vấn thực tế phức tạp hơn nhiều so với Ngày 1.

1. Lý thuyết cốt lõi Ngày 2
   A. Kết hợp logic phức tạp (AND, OR, NOT)
   Khi điều kiện lọc không chỉ là một tiêu chuẩn đơn lẻ:

AND: Tất cả các điều kiện phải đúng cùng lúc.

OR: Chỉ cần ít nhất một điều kiện đúng.

NOT: Phủ định (đảo ngược) điều kiện.

⚠️ Lưu ý về thứ tự ưu tiên: Trong SQL, AND được tính trước OR. Nếu muốn nhóm điều kiện OR, bạn bắt buộc phải dùng dấu ngoặc đơn ().

Ví dụ: WHERE (Country = 'USA' OR Country = 'Canada') AND City = 'Paris'

B. Tìm kiếm chuỗi gần đúng (LIKE & ILIKE)
Dùng khi bạn không nhớ chính xác toàn bộ từ cần tìm mà chỉ biết một phần mẫu chuỗi (Pattern Matching).

%: Đại diện cho 0 hoặc nhiều ký tự bất kỳ.

\_: Đại diện cho đúng 1 ký tự bất kỳ.
Phân biệt Case-Sensitivity:LIKE: Phân biệt hoa/thường trong một số CSDL (như PostgreSQL).ILIKE: Không phân biệt hoa/thường (dành riêng cho PostgreSQL, ví dụ: 'love%' tìm được cả 'Love' và 'LOVE'). Trong MySQL, LIKE mặc định không phân biệt hoa/thường.C. Sắp xếp kết quả (ORDER BY) & Giới hạn (LIMIT)Mặc định CSDL trả kết quả không theo thứ tự cố định. Để sắp xếp và cắt kết quả:ORDER BY column1 ASC/DESC, column2 ASC/DESCASC (Ascending): Sắp xếp tăng dần (A $\rightarrow$ Z, 1 $\rightarrow$ 9) — Mặc định nếu không ghi.DESC (Descending): Sắp xếp giảm dần (Z $\rightarrow$ A, 9 $\rightarrow$ 1).LIMIT N: Chỉ lấy ra $N$ dòng đầu tiên của kết quả.D. Thứ tự viết & Thứ tự thực thi câu lệnh SQL (Rất quan trọng!)Bây giờ câu lệnh SQL của bạn đã dài hơn, hãy nhớ thứ tự các mệnh đề:
SELECT [Cột muốn lấy / DISTINCT]
FROM [Bảng dữ liệu]
WHERE [Điều kiện lọc dữ liệu]
ORDER BY [Cột sắp xếp ASC/DESC]
LIMIT [Số lượng dòng muốn lấy];
SELECT
FirstName AS Ten,
LastName AS Ho,
PostalCode AS "Ma Buu Dien"
FROM customer AS c;

-- Ví dụ: Mỗi trang hiển thị 10 bài hát (Size = 10)

-- Trang 1: Lấy 10 bài đầu tiên (Bỏ qua 0 bài)
SELECT TrackId, Name FROM track ORDER BY TrackId LIMIT 10 OFFSET 0;

-- Trang 2: Lấy 10 bài tiếp theo (Bỏ qua 10 bài của trang 1)
SELECT TrackId, Name FROM track ORDER BY TrackId LIMIT 10 OFFSET 10;

-- Trang 3: Lấy 10 bài tiếp theo (Bỏ qua 20 bài của trang 1 và 2)
SELECT TrackId, Name FROM track ORDER BY TrackId LIMIT 10 OFFSET 20;
Công thức phân trang thực tế:Muốn lấy dữ liệu cho Trang thứ P, mỗi trang có S dòng:
LIMIT S
OFFSET((P-1)XS)

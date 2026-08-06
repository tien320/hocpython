SELECT column1, SUM(column2)
FROM table_name
WHERE condition                       -- 1. Lọc dòng ban đầu
GROUP BY column1                      -- 2. Gom nhóm dữ liệu
HAVING SUM(column2) > 1000            -- 3. Lọc nhóm SAU KHI đã gom nhóm (khác với WHERE)
ORDER BY column1 DESC;                -- 4. Sắp xếp kết quả (ASC/DESC)

 3. Các hàm xử lý dữ liệu thông dụng (Built-in Functions)
 Hàm xử lý Chuỗi & Ngày thángChuỗi: 
 UPPER('abc') $\rightarrow$ 'ABC', 
 LOWER('ABC') $\rightarrow$ 'abc', 
 SUBSTR('Oracle', 1, 3) $\rightarrow$ 'Ora', 
 LENGTH('SQL') $\rightarrow$ 
 3.Xử lý NULL:NVL(expr1, expr2): 
 Nếu expr1 NULL thì trả về expr2.
 Ngày tháng & Chuyển đổi kiêu dữ liệu (Đặc thù Oracle):
 SYSDATE: Ngày giờ hiện tại của server.
 TO_DATE('2026-08-05', 'YYYY-MM-DD'): Chuyển Chuỗi $\rightarrow$ Ngày.
 TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI:SS'): Chuyển Ngày/Số $\rightarrow$ Chuỗi.
 Hàm Gom nhóm (Aggregate Functions)Dùng chung với GROUP BY: COUNT(), SUM(), AVG(), MIN(), MAX().

 SELECT first_name, salary,
       CASE 
           WHEN salary >= 10000 THEN 'High'
           WHEN salary >= 5000  THEN 'Medium'
           ELSE 'Low'
       END AS salary_level
FROM employees;
1. Sắp xếp, Phân trang, Lọc trùng & Đặt Alias
ORDER BY (Sắp xếp)
Dùng để sắp xếp kết quả theo thứ tự tăng dần (ASC - mặc định) hoặc giảm dần (DESC).
SELECT first_name, salary 
FROM employees 
ORDER BY salary DESC, first_name ASC;
DISTINCT (Loại bỏ trùng lặp)
Lọc ra các giá trị duy nhất (không trùng nhau).
SELECT DISTINCT job_id FROM employees;
Đặt Alias (AS)
Đổi tên hiển thị cho cột hoặc đặt tên ngắn cho bảng.

Tên cột: Dùng AS (có thể bỏ từ khóa AS). Nếu tên có khoảng trắng hoặc viết hoa/thường cố định, bọc trong dấu nháy đôi " ".

Tên bảng: Không dùng AS (Oracle không hỗ trợ AS cho alias bảng).
SELECT e.first_name AS "Tên Nhân Viên", e.salary * 12 AS annual_salary
FROM employees e;
hân trang: OFFSET & FETCH (Oracle 12c trở lên)
Lưu ý: Oracle không dùng LIMIT. Dùng cú pháp OFFSET ... FETCH tiêu chuẩn:
SELECT emp_id, first_name, salary
FROM employees
ORDER BY salary DESC
OFFSET 10 ROWS            -- Bỏ qua 10 dòng đầu
FETCH NEXT 5 ROWS ONLY;   -- Lấy 5 dòng tiếp theo
2. Kiểu dữ liệu phổ biến & Ép kiểu trong Oracle
Kiểu dữ liệu chính
Kiểu dữ liệu,Mô tả,Ví dụ
VARCHAR2(size),"Chuỗi độ dài linh hoạt (Oracle dùng VARCHAR2, không dùng VARCHAR).",VARCHAR2(100)
"NUMBER(p, s)","Số. p là tổng số chữ số (precision), s là số chữ số thập phân (scale).","NUMBER(10, 2) (tối đa 99,999,999.99)"
DATE,Chứa ngày + giờ (Ngày/Tháng/Năm Giờ:Phút:Giây).,2026-08-05 11:00:40
TIMESTAMP,Tương tự DATE nhưng chính xác đến phần nghìn giây (fractional seconds).,2026-08-05 11:00:40.123456
Ép kiểu dữ liệu (Conversion Functions)
Oracle dùng 3 hàm chuyển đổi chính:

          TO_CHAR             TO_DATE
  NUMBER --------> VARCHAR2 ----------> DATE
         <--------          <----------
          TO_NUMBER           TO_CHAR
 
TO_CHAR: Chuyển Số hoặc Ngày $\rightarrow$ Chuỗi định dạng.
SELECT TO_CHAR(SYSDATE, 'DD/MM/YYYY HH24:MI:SS') FROM dual;
SELECT TO_CHAR(1234567.89, '$999,999,999.99') FROM dual; -- Output: $1,234,567.89
TO_DATE: Chuyển Chuỗi $\rightarrow$ Kiểu Ngày (DATE).
SELECT TO_DATE('05/08/2026', 'DD/MM/YYYY') FROM dual;
TO_NUMBER: Chuyển Chuỗi số $\rightarrow$ Kiểu Số (NUMBER).
SELECT TO_NUMBER('1500') + 500 FROM dual;
3. Các hàm xử lý chuỗi trong Oracle
Lưu ý: Oracle dùng SUBSTR (không phải SUBSTRING) và dùng || hoặc CONCAT để nối chuỗi.

LOWER(str) / UPPER(str): Chuyển thành chữ thường / chữ hoa.
SELECT LOWER('Oracle'), UPPER('Oracle') FROM dual; -- 'oracle', 'ORACLE'
TRIM(str): Cắt khoảng trắng 2 đầu. (Có thêm LTRIM cắt bên trái, RTRIM cắt bên phải).
SELECT TRIM('  hello  ') FROM dual; -- 'hello'
SUBSTR(str, start, length): Cắt chuỗi từ vị trí start, lấy length ký tự.
SELECT SUBSTR('Oracle SQL', 1, 6) FROM dual; -- 'Oracle'
Nối chuỗi (|| hoặc CONCAT):

Toán tử || (Khuyên dùng vì nối được nhiều chuỗi):
SELECT first_name || ' ' || last_name AS full_name FROM employees;
Hàm CONCAT(str1, str2) (Oracle chỉ cho phép ghép 2 chuỗi 1 lúc):
SELECT CONCAT(first_name, last_name) FROM employees;
4. Các hàm Ngày - Tháng trong Oracle
Lưu ý: Oracle không có NOW() (dùng SYSDATE hoặc CURRENT_TIMESTAMP) và không có DATE_TRUNC (dùng TRUNC).

Ngày hiện tại:

SYSDATE: Ngày giờ hệ thống của Server.

CURRENT_DATE: Ngày giờ theo time zone của Session.
SELECT SYSDATE FROM dual;
(Lưu ý: Bảng DUAL là bảng ảo mặc định của Oracle dùng để chạy các câu lệnh test không cần bảng thật).

Cắt phần thừa của ngày (TRUNC thay cho DATE_TRUNC):

Reset thời gian về 00:00:00 hoặc làm tròn về đầu tháng/đầu năm.
SELECT TRUNC(SYSDATE) FROM dual;        -- Trả về ngày hiện tại với giờ là 00:00:00
SELECT TRUNC(SYSDATE, 'MM') FROM dual;  -- Trả về ngày đầu tiên của tháng hiện tại
SELECT TRUNC(SYSDATE, 'YYYY') FROM dual;-- Trả về ngày 01/01 của năm hiện tại
Trích xuất thông tin ngày (EXTRACT hoặc TO_CHAR):

EXTRACT(unit FROM date):
SELECT EXTRACT(YEAR FROM SYSDATE) AS current_year,
       EXTRACT(MONTH FROM SYSDATE) AS current_month
FROM dual;
Hoặc dùng TO_CHAR linh hoạt hơn:
SELECT TO_CHAR(SYSDATE, 'YYYY') AS nam,
       TO_CHAR(SYSDATE, 'Q') AS quy
FROM dual;
1. Các hàm số học cơ bản (ROUND, CEIL, FLOOR)
Oracle hỗ trợ các hàm làm tròn số rất trực quan:
SELECT 
    ROUND(45.678, 2) AS round_val,
    CEIL(45.1)       AS ceil_val,
    FLOOR(45.9)      AS floor_val
FROM dual;
2. Bản chất giá trị NULL trong OracleNULL không phải là số 0, cũng không phải là chuỗi rỗng '' (Trong Oracle, chuỗi rỗng '' tự động được coi là NULL). 
NULL có nghĩa là không xác định (Unknown) hoặc thiếu dữ liệu.3 quy tắc "vàng" về NULL:
Phép tính toán học với NULL luôn trả về 
NULL:$10 + \text{NULL} = \text{NULL}$$
100 * \text{NULL} = \text{NULL}$
So sánh với NULL bằng toán tử (=, <>, >, <) luôn trả về UNKNOWN (False):
salary = NULL $\rightarrow$ Sai (phải dùng salary IS NULL)salary <> NULL $\rightarrow$ Sai (phải dùng salary IS NOT NULL)
Các hàm gom nhóm (Aggregate Functions) tự động bỏ qua NULL:
SUM(salary), AVG(salary) sẽ bỏ qua các dòng có salary là NULL.
Ngoại lệ: COUNT(*) đếm tất cả các dòng (kể cả dòng chứa NULL), còn COUNT(column) chỉ đếm các dòng mà cột đó không NULL.
3. Xử lý NULL an toàn (COALESCE, NULLIF, NVL, NVL2)
Để tránh việc dữ liệu bị biến thành NULL khi tính toán hoặc hiển thị, Oracle cung cấp các hàm xử lý NULL chuẩn SQL:A. COALESCE(expr1, expr2, ..., exprN)
Cách hoạt động: Trả về giá trị ĐẦU TIÊN KHÔNG NULL trong danh sách truyền vào.
Ưu điểm: Đạt chuẩn ANSI SQL (dùng được trên mọi Database như SQL Server, MySQL, Postgres) và nhận được nhiều tham số.
-- Nếu commission_pct NULL thì lấy salary, nếu salary cũng NULL thì lấy 0
SELECT first_name, COALESCE(commission_pct, salary, 0) AS final_val
FROM employees;
B. NULLIF(expr1, expr2)
Cách hoạt động:

Trả về NULL nếu expr1 = expr2.

Trả về expr1 nếu expr1 <> expr2.

Ứng dụng thực tế lớn nhất: Tránh lỗi chia cho số 0 (ORA-01476: divisor is equal to zero).
-- Nếu total_sales = 0, NULLIF trả về NULL -> kết quả phép chia sẽ là NULL thay vì bị gián đoạn do LỖI CHIA CHO 0
SELECT total_amount / NULLIF(total_sales, 0) AS avg_sale
FROM sales_summary;
C. Các hàm đặc thù của Oracle (NVL và NVL2)
Dù COALESCE và NULLIF là chuẩn chung, trong các dự án Oracle thực tế bạn sẽ bắt gặp NVL và NVL2 rất nhiều:

NVL(expr1, replacement): Nếu expr1 NULL thì trả về replacement (Viết ngắn gọn cho trường hợp 2 tham số của COALESCE).

SELECT salary + NVL(commission_pct, 0) FROM employees;
NVL2(expr1, if_not_null, if_null): Nếu expr1 NOT NULL thì trả về if_not_null, ngược lại trả về if_null.
SELECT first_name, 
       NVL2(commission_pct, 'Có hoa hồng', 'Không có hoa hồng') AS status
FROM employees;






























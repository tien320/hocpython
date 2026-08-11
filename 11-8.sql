-- ====================
-- Bài 1: WINDOW FUNCTION - Top 3 bài hát doanh thu cao nhất theo thể loại
-- Mục tiêu: Sử dụng hàm cửa sổ để xếp hạng doanh thu mỗi bài, giữ lại chi tiết từng dòng.
-- LÝ THUYẾT: Window function cho phép tính toán theo cửa sổ phân vùng mà không gộp dòng lại.
-- ====================
WITH trackvalue AS (
SELECT 
g.NAME AS genre_name,
t.NAME AS track_name, 
SUM(il.UNITPRICE * il.QUANTITY ) AS trackvalue,
dense_rank() OVER (
PARTITION BY g.GENREID 
ORDER BY SUM(il.UNITPRICE * il.QUANTITY ) DESC 
) AS rank
FROM GENRE g 
JOIN TRACK t ON t.GENREID = g.GENREID 
JOIN INVOICELINE il ON il.TRACKID = t.TRACKID
GROUP BY g.GENREID ,g.NAME ,t.TRACKID ,t.NAME 
)
SELECT 
GENRE_NAME ,TRACK_NAME ,TRACKVALUE ,"RANK" 
FROM trackvalue 
WHERE RANK <= 3
ORDER BY GENRE_NAME ,TRACKVALUE ,"RANK" DESC;
-- bai2
SELECT 
c.CUSTOMERID ,c.FIRSTNAME ||' '|| c.LASTNAME AS customer_name,
i.INVOICEID ,i.INVOICEDATE , i.TOTAL AS current_total,
SUM(i.TOTAL ) over(
PARTITION BY c.CUSTOMERID 
ORDER BY i.INVOICEDATE ,i.INVOICEID 
) AS running_total
FROM CUSTOMER c 
JOIN INVOICE i ON i.CUSTOMERID = c.CUSTOMERID 
ORDER BY c.CUSTOMERID , i.INVOICEDATE ,i.INVOICEID ;
-- ====================
-- Bài 2: WINDOW FUNCTION - Tổng doanh thu tích lũy theo khách hàng
-- Mục tiêu: Dùng SUM(...) OVER(...) để tính tổng lũy kế mỗi hóa đơn trong cùng khách hàng.
-- LÝ THUYẾT: Aggregate window function giữ từng dòng chi tiết và tính toán trên toàn bộ cửa sổ phân vùng.
-- ====================
--bai3
SELECT
i.INVOICEID , i.INVOICEDATE , i.TOTAL AS current_total,
c.CUSTOMERID ,
LAG(i.TOTAL ,1,0) OVER (
PARTITION BY c.CUSTOMERID 
ORDER BY i.INVOICEID ,i.INVOICEDATE 
) AS previous_total,
i.TOTAL  - LAG(i.TOTAL ,1,0) OVER (
PARTITION BY c.CUSTOMERID 
ORDER BY i.CUSTOMERID ,i.INVOICEDATE 
) AS difference
FROM INVOICE i 
JOIN CUSTOMER c ON c.CUSTOMERID = i.CUSTOMERID 
ORDER BY c.CUSTOMERID ,i.INVOICEID ,i.INVOICEDATE;
-- ====================
-- Bài 3: WINDOW FUNCTION - So sánh hóa đơn hiện tại với hóa đơn trước đó
-- Mục tiêu: Sử dụng LAG để lấy giá trị hóa đơn trước và tính hiệu số cho mỗi khách hàng.
-- LÝ THUYẾT: LAG/LEAD truy cập giá trị của hàng khác trong cùng cửa sổ mà không cần self join.
-- ====================
-- ====================
-- Bài 4: VIEW - Tạo các view báo cáo thông tin khách hàng và doanh thu nhân viên
-- Mục tiêu: Sử dụng VIEW để đóng gói logic truy vấn, tạo bảng ảo tái sử dụng.
-- LÝ THUYẾT: VIEW là bảng ảo được định nghĩa bởi SELECT, giúp tổ chức truy vấn và bảo mật dữ liệu.
-- ====================
CREATE VIEW customerprofile AS
SELECT c.customerid, c.firstname, c.lastname, c.country 
FROM CUSTOMER c 
LEFT JOIN EMPLOYEE e ON e.employeeid = c.supportrepid;
SELECT * FROM customerprofile;
DROP VIEW customerprofile;
--
CREATE VIEW employee_sale as
SELECT 
e.EMPLOYEEID ,e.FIRSTNAME ,e.LASTNAME,
count(i.INVOICEID ) AS tongsohoadon, SUM(i.TOTAL ) AS tonghoadon
FROM EMPLOYEE e 
JOIN CUSTOMER c ON c.SUPPORTREPID = e.EMPLOYEEID 
JOIN INVOICE i ON i.CUSTOMERID = c.CUSTOMERID 
GROUP BY e.EMPLOYEEID , e.FIRSTNAME ,e.LASTNAME ;
SELECT * FROM employee_sale;
DROP VIEW employee_sale;
--
CREATE VIEW track_detail as
SELECT 
t.TRACKID ,t.NAME AS track_name ,g.NAME AS genre_name , ROUND(t.MILLISECONDS/60000,2 ) AS duration
FROM TRACK t 
LEFT JOIN GENRE g ON g.GENREID = t.GENREID;
CREATE VIEW track_summary as
SELECT td.genre_name, count(td.trackid) AS total_track, AVG(td.duration) AS avgduration
FROM track_detail td
WHERE td.genre_name IS NOT NULL 
GROUP BY td.genre_name;
SELECT * FROM track_detail;
SELECT * FROM track_summary;
DROP VIEW track_detail;
DROP VIEW track_summary;
-- ====================
-- Bài 5: PROCEDURE - Cập nhật địa chỉ khách hàng
-- Mục tiêu: Viết procedure nhận tham số và thay đổi dữ liệu bảng CUSTOMER.
-- LÝ THUYẾT: PROCEDURE là chương trình con lưu trong Oracle để thực hiện tác vụ với tham số IN/OUT và logic điều kiện.
-- ====================
CREATE PROCEDURE update_customer_add (
p_customerid IN NUMBER,
p_newadd IN varchar2,
p_newcity IN varchar2,
p_newcountry IN varchar2
) AS
BEGIN 
	UPDATE customer
	SET address = p_newadd,
	city = p_newcity,
	country = p_newcountry
	WHERE customerid = p_customerid;
COMMIT;
END;
BEGIN
    update_customer_add(
        5,
        '123 Nguyen Trai',
        'Ha Noi',
        'Vietnam'
    );
END;
SELECT * FROM customer WHERE customerid =5;
-- ====================
-- Bài 6: PROCEDURE - Thêm thể loại mới và trả về GenreId
-- Mục tiêu: Kiểm tra trùng tên thể loại, sau đó chèn mới và trả về ID mới.
-- LÝ THUYẾT: PROCEDURE có thể dùng OUT parameter để trả giá trị ra ngoài và xử lý lỗi bằng raise_application_error.
-- ====================
CREATE PROCEDURE add_new_genre(
p_genrename IN varchar2,
p_newgenreid OUT number
) AS count_number
BEGIN 
	SELECT count(*) INTO count_number
	FROM genre
	WHERE lower(name) = lower(p_genrename);
    IF count_number >0 THEN 
    raise_application_error(-20001, 'Thể loại đã tồn tại')
    ELSE 
    SELECT 
    nvl(max(genreid),0) +1 INTO p_newgenreid
    FROM genre;
    INSERT INTO genre(genreid,name) VALUES (p_newgenreid,p_genrename);
    COMMIT;
    END IF;
 END;
-- ====================
-- Bài 7: PROCEDURE - Tra cứu bài hát theo tên nghệ sĩ
-- Mục tiêu: Mở con trỏ REF CURSOR để trả về danh sách track theo tên nghệ sĩ.
-- LÝ THUYẾT: PROCEDURE với SYS_REFCURSOR cho phép trả về tập kết quả động từ PL/SQL.
-- ====================
CREATE PROCEDURE get_track_by_artist (
p_artistname IN varchar2,
p_cursor OUT SYS_REFCURSOR
) AS 
BEGIN 
	OPEN p_cursor FOR 
	SELECT 
	t.trackid,
	t.name AS track_name,
	a.title AS album_title
	FROM track t
	JOIN album a ON a.albumid = t.albumid
	JOIN artist ar ON ar.artistid = a.artistid
	WHERE lower(ar.name) LIKE '%' || lower(p_artistname) || '%';
END;
-- ====================
-- Bài 8: PACKAGE - Nhóm hàm và thủ tục phân tích Chinook
-- Mục tiêu: Tạo package chứa hàm đếm album và thủ tục giảm giá theo thể loại.
-- LÝ THUYẾT: PACKAGE nhóm các hàm/procedure liên quan trong một thư viện. Phần specification khai báo interface, package body chứa cài đặt.
-- ====================
CREATE PACKAGE pkg_chinook_analytics AS
    FUNCTION fn_album_count(p_artist_id IN NUMBER) RETURN NUMBER;
    PROCEDURE sp_apply_discount(p_genre_id IN NUMBER, p_discount_percent IN NUMBER);
END pkg_chinook_analytics;
/

-- ====================
-- Package Body: Định nghĩa chi tiết các thủ tục và hàm đã khai báo ở phần specification.
-- LÝ THUYẾT: Package body chứa mã PL/SQL thực thi, riêng phần specification chỉ khai báo giao diện.
-- ====================
CREATE OR REPLACE PACKAGE BODY pkg_chinook_analytics AS
    FUNCTION fn_album_count(p_artist_id IN NUMBER) RETURN NUMBER IS
        v_count NUMBER := 0;
    BEGIN
        SELECT COUNT(*) INTO v_count FROM Album WHERE ArtistId = p_artist_id;
        RETURN v_count;
    END fn_album_count;

    PROCEDURE sp_apply_discount(p_genre_id IN NUMBER, p_discount_percent IN NUMBER) IS
    BEGIN
        UPDATE Track
        SET UnitPrice = UnitPrice * (1 - p_discount_percent / 100)
        WHERE GenreId = p_genre_id;
        COMMIT;
    END sp_apply_discount;
END pkg_chinook_analytics;
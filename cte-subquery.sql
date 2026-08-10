-- bai1: Tìm track có thời lượng ngắn hơn lớn hơn thời lượng trung bình của tất cả track.
-- Yêu cầu: sử dụng subquery trong WHERE để so sánh mỗi track với giá trị trung bình chung.
SELECT 
t.NAME ,t.MILLISECONDS 
FROM TRACK t 
WHERE t.MILLISECONDS >(
SELECT avg(t2.MILLISECONDS )
FROM TRACK t2 
);
-- bai2: Liệt kê track thuộc thể loại Rock hoặc Jazz.
-- Yêu cầu: sử dụng subquery trong mệnh đề WHERE để lọc theo GENREID.
SELECT 
t.TRACKID ,t.NAME ,t.UNITPRICE 
FROM TRACK t 
WHERE t.GENREID in (
SELECT
g.GENREID
FROM GENRE g 
WHERE g.NAME IN ('Rock','Jazz')
);
-- bai3: Hiển thị khách hàng có quốc gia xuất hiện trong bảng nhân viên.
-- Yêu cầu: sử dụng subquery để kiểm tra giá trị COUNTRY có nằm trong danh sách quốc gia của nhân viên hay không.
SELECT 
c.CUSTOMERID ,c.COUNTRY ,c.FIRSTNAME ||' '|| c.LASTNAME AS full_name
FROM CUSTOMER c 
WHERE c.COUNTRY IN(
SELECT distinct
e.COUNTRY 
FROM EMPLOYEE e
WHERE c.COUNTRY IS NOT NULL   
);
-- bai4: Tìm album có tổng giá tiền track cao nhất.
-- Yêu cầu: sử dụng subquery với GROUP BY và ORDER BY để chọn ALBUMID đứng đầu.
SELECT 
a.ALBUMID ,a.TITLE 
FROM ALBUM a 
WHERE a.ALBUMID =(
SELECT
t.ALBUMID   
FROM TRACK t
GROUP BY t.ALBUMID 
ORDER BY sum(t.UNITPRICE ) DESC
FETCH FIRST 1 ROWS only
);
-- bai5: Liệt kê khách hàng không mua file âm thanh MPEG.
-- Yêu cầu: sử dụng subquery với NOT IN và JOIN để loại trừ khách hàng có đơn hàng chứa định dạng MPEG audio file.
SELECT
c.CUSTOMERID ,c.FIRSTNAME ,c.LASTNAME 
FROM customer c
WHERE c.CUSTOMERID NOT IN (
SELECT 
i.CUSTOMERID 
FROM INVOICE i
JOIN INVOICELINE i2 ON i2.INVOICEID =i.INVOICEID 
JOIN track t ON i2.TRACKID =t.TRACKID 
JOIN MEDIATYPE m ON t.MEDIATYPEID = m.MEDIATYPEID 
WHERE m.NAME IN ('MPEG audio file')
);
-- bai6: Tìm nghệ sĩ không có album nào trong bảng Album.
-- Yêu cầu: sử dụng NOT EXISTS để kiểm tra không tồn tại album liên quan.
SELECT ArtistId, Name 
FROM Artist a 
WHERE NOT EXISTS (
    SELECT 1 
    FROM Album al 
    WHERE al.ArtistId = a.ArtistId
);
-- bai7: Tìm track dài nhất cho mỗi album.
-- Yêu cầu: dùng subquery correlated trong WHERE để so sánh với giá trị MAX theo ALBUMID.
SELECT t.TRACKID ,t.NAME ,t.ALBUMID ,t.MILLISECONDS  
FROM TRACK t 
WHERE t.MILLISECONDS = (
SELECT
MAX(t2.MILLISECONDS) 
FROM TRACK t2 
WHERE t.ALBUMID  = t2.ALBUMID
);
-- bai8: Tìm thể loại có doanh thu cao nhất từ track bán ra.
-- Yêu cầu: sử dụng subquery để tìm GENREID có tổng doanh thu lớn nhất, sau đó map về tên thể loại.
SELECT 
g.NAME 
FROM GENRE g 
WHERE g.GENREID = (
SELECT 
t.GENREID 
FROM TRACK t
JOIN INVOICELINE i ON i.TRACKID = t.TRACKID 
GROUP BY t.GENREID 
ORDER BY sum(i.UNITPRICE * i.QUANTITY ) DESC 
FETCH FIRST 1 ROWS only
);
-- bai9: Tìm nhân viên có ít nhất một khách hàng hỗ trợ tại USA với hóa đơn trên 10.
-- Yêu cầu: sử dụng EXISTS lồng nhau để kiểm tra quan hệ ba bảng Employee - Customer - Invoice.
SELECT 
e.EMPLOYEEID ,e.FIRSTNAME ,e.LASTNAME 
FROM EMPLOYEE e 
WHERE EXISTS(
SELECT 1 
FROM CUSTOMER c
WHERE c.SUPPORTREPID = e.EMPLOYEEID 
AND c.COUNTRY ='USA'
AND EXISTS (
SELECT 1 
FROM INVOICE i
WHERE i.CUSTOMERID = c.CUSTOMERID 
AND i.TOTAL >10
)
);
-- bai1 (CTE): So sánh giá tiền của track với giá trung bình theo thể loại.
-- Yêu cầu: chuyển correlated subquery sang CTE, sau đó lọc track có giá cao hơn trung bình genre.
-- Code cũ: Dùng Correlated Subquery ở WHERE
SELECT t1.Name, t1.AlbumId, t1.GenreId, t1.UnitPrice
FROM Track t1
WHERE t1.UnitPrice > (
    SELECT AVG(t2.UnitPrice)
    FROM Track t2
    WHERE t2.GenreId = t1.GenreId
);
-- CTE: Tính giá trung bình của tất cả track và chọn track có giá lớn hơn giá trung bình đó.
WITH avgprice AS (
SELECT avg(t.UNITPRICE ) AS avg
FROM TRACK t 
)
SELECT t.TRACKID ,t.NAME ,t.UNITPRICE 
FROM TRACK t , avgprice a
WHERE t.UNITPRICE > a.avg;
-- bai2 (CTE): Lấy 3 khách hàng Mỹ có tổng chi tiêu cao nhất so với trung bình.
-- Yêu cầu: sử dụng CTE để tránh lặp lại tính toán tổng chi tiêu cho mỗi khách hàng.
-- Code cũ: Nhân bản logic SUM(Total) ở 2 nơi khác nhau
SELECT c.CustomerId, c.FirstName, c.LastName, CustTotal.TotalSpent
FROM Customer c
JOIN (
    SELECT CustomerId, SUM(Total) AS TotalSpent
    FROM Invoice
    GROUP BY CustomerId
) CustTotal ON c.CustomerId = CustTotal.CustomerId
WHERE CustTotal.TotalSpent > (
    SELECT AVG(TotalSpent)
    FROM (
        SELECT SUM(Total) AS TotalSpent
        FROM Invoice
        GROUP BY CustomerId
    )
)
ORDER BY CustTotal.TotalSpent DESC;
-- CTE: Xây dựng danh sách khách hàng Mỹ và tổng chi tiêu của họ, rồi chọn 3 người chi nhiều nhất.
WITH USAcustomer AS (
SELECT c.CUSTOMERID ,c.FIRSTNAME ,c.LASTNAME  FROM CUSTOMER c 
WHERE c.COUNTRY = 'USA'
),
customerspending as(
SELECT uc.CUSTOMERID ,uc.FIRSTNAME ,uc.LASTNAME ,sum(i.TOTAL ) AS total FROM USAcustomer uc
JOIN INVOICE i ON i.CUSTOMERID = uc.CUSTOMERID 
GROUP BY uc.CUSTOMERID , uc.FIRSTNAME ,uc.LASTNAME 
)
SELECT CUSTOMERID ,FIRSTNAME ,LASTNAME ,TOTAL  FROM customerspending 
ORDER BY TOTAL DESC 
FETCH FIRST 3 ROWS ONLY;
-- bai3 (CTE): Tìm thể loại track giá trên trung bình bằng cách tách logic ra thành CTE rõ ràng.
-- Yêu cầu: đơn giản hóa subquery lồng nhau bằng cấu trúc CTE.
-- Code cũ: Subquery lồng 3 lớp rối mắt
SELECT Name 
FROM Artist 
WHERE ArtistId = (
    SELECT ArtistId 
    FROM Album 
    WHERE AlbumId = (
        SELECT AlbumId 
        FROM Track 
        WHERE TrackId IN (
            SELECT il.TrackId 
            FROM InvoiceLine il
            JOIN Track t ON il.TrackId = t.TrackId
            JOIN Genre g ON t.GenreId = g.GenreId
            WHERE g.Name = 'Rock'
        )
        GROUP BY AlbumId
        ORDER BY SUM(UnitPrice) DESC
        FETCH FIRST 1 ROWS ONLY
    )
);
-- CTE: Tính giá trung bình theo genre rồi chọn track có giá cao hơn trung bình genre đó.
WITH genreavgprice AS (
SELECT GENREID ,avg(UNITPRICE) AS avg  FROM track
GROUP BY GENREID 
)
SELECT t.GENREID ,t.ALBUMID ,t.NAME ,t.UNITPRICE   FROM TRACK t 
JOIN genreavgprice g ON g.GENREID = t.GENREID 
WHERE t.UNITPRICE > g.AVG ;
-- bai4 (CTE): Tìm khách hàng có tổng hóa đơn cao hơn tổng trung bình của tất cả khách hàng.
-- Yêu cầu: chuyển subquery trong SELECT sang CTE tính tổng và trung bình trước.
-- Code cũ: Dùng Subquery ngay trên mệnh đề SELECT
SELECT 
    t.TrackId,
    t.Name,
    t.UnitPrice,
    (
        SELECT AVG(t2.UnitPrice) 
        FROM Track t2 
        WHERE t2.AlbumId = t.AlbumId
    ) AS AlbumAvgPrice
FROM Track t
WHERE t.AlbumId IS NOT NULL
FETCH FIRST 10 ROWS ONLY;
-- CTE: Tính tổng chi tiêu theo khách hàng và trung bình tổng chi tiêu để lọc ra khách hàng chi nhiều hơn trung bình.
WITH customerspending AS (
SELECT CUSTOMERID  ,sum(TOTAL) AS total  FROM INVOICE  
GROUP BY CUSTOMERID 
),
overallavg AS (
SELECT avg(TOTAL ) AS avg FROM customerspending  
)
SELECT c.CUSTOMERID ,c.FIRSTNAME ,c.LASTNAME, cs.TOTAL 
FROM customerspending cs
JOIN CUSTOMER c ON c.CUSTOMERID  = cs.CUSTOMERID
CROSS JOIN overallavg oa 
WHERE cs.TOTAL > oa.AVG 
ORDER BY cs.TOTAL DESC;
-- bai5 (CTE): Tìm nhân viên hỗ trợ khách hàng có hóa đơn năm 2011 trên 40.
-- Yêu cầu: tránh subquery lồng nhiều cấp bằng cách tách logic ra thành CTE rõ ràng.
-- CODE CŨ CẦN REFACTOR:
SELECT EmployeeId, FirstName, LastName
FROM Employee
WHERE EmployeeId IN (
    SELECT SupportRepId
    FROM Customer
    WHERE CustomerId IN (
        SELECT CustomerId
        FROM Invoice
        WHERE EXTRACT(YEAR FROM InvoiceDate) = 2011
        GROUP BY CustomerId
        HAVING SUM(Total) > 40.00
    )
);
-- CTE: Tính giá trung bình theo album rồi lấy 10 track đầu tiên kèm giá trung bình album.
WITH albumstat AS ( 
SELECT ALBUMID ,avg(UNITPRICE ) AS avgalb FROM track
WHERE ALBUMID IS NOT NULL 
GROUP BY ALBUMID 
)
SELECT t.TRACKID ,t.NAME ,ast.AVGALB   FROM TRACK t 
JOIN albumstat ast ON ast.ALBUMID = t.ALBUMID 
FETCH FIRST 10 ROWS ONLY;
-- bai6 (CTE): Tìm nhân viên hỗ trợ khách hàng năm 2011 có tổng hóa đơn hơn 40.
-- Yêu cầu: chuyển subquery lồng nhiều cấp sang CTE để mã dễ đọc hơn.
--subquery
-- CODE CŨ CẦN REFACTOR:
SELECT EmployeeId, FirstName, LastName
FROM Employee
WHERE EmployeeId IN (
    SELECT SupportRepId
    FROM Customer
    WHERE CustomerId IN (
        SELECT CustomerId
        FROM Invoice
        WHERE EXTRACT(YEAR FROM InvoiceDate) = 2011
        GROUP BY CustomerId
        HAVING SUM(Total) > 40.00
    )
);
-- CTE: Xác định khách hàng có hóa đơn năm 2011 trên 40 và tìm nhân viên hỗ trợ tương ứng.
WITH value2011 AS  (
SELECT CUSTOMERID   FROM invoice
WHERE EXTRACT(YEAR FROM INVOICEDATE) = 2011
GROUP BY CUSTOMERID 
HAVING (SUM(TOTAL )) > 40
),
supportemployee AS (
SELECT c.SUPPORTREPID  FROM CUSTOMER c 
JOIN value2011 v ON v.CUSTOMERID = c.CUSTOMERID 
WHERE c.SUPPORTREPID IS NOT NULL 
)
SELECT e.EMPLOYEEID ,e.FIRSTNAME ,e.LASTNAME  FROM EMPLOYEE e 
JOIN supportemployee se ON se.SUPPORTREPID = e.EMPLOYEEID;


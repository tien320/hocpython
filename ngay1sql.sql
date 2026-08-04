-- NGÀY 1 học các truy vấn cơ bản và tạo csdl
-- Học SELECT FROM WHERE và các phép so sánh (= <> > < BETWEEN IN)
use chinook;
-- Lấy ra 10 khách hàng đầu tiên trong bảng customer
SELECT * 
FROM customer 
LIMIT 10;
-- bai1
select Firstname,Lastname,Title,Email
from employee
where Title = 'Sales Support Agent';
-- bai2
select CustomerId,Firstname,Lastname,Country
from customer
where Country != 'USA';
-- bai3
select AlbumID,Title 
from album
where ArtistID = 22;
-- bai4
select InvoiceId,InvoiceDate,total
from invoice
where total >= 10;
-- bai5
select name,bytes 
from track 
where bytes < 2000000;
-- bai6
select CustomerId,Firstname,Lastname,Company
from customer 
where CustomerId <15;
-- bai7
select name,composer,Milliseconds
from track
where Milliseconds between 200000 and 300000;
-- bai8 
select InvoiceId,InvoiceDate,total
from invoice
where InvoiceDate between '2021-01-01' and '2021-06-30';
-- bai9
select Firstname,Lastname,city,country
from customer
where city in ('London','Paris','Berlin','Rome');
-- bai 10
select Name,MediaTypeId,UnitPrice
from track
where MediaTypeId in (1,2,3)
and UnitPrice > 0.99;

-- Ngày 2 
-- Học ORDER BY LIMIT OFFSET DISTINCT đặt Alias (AS)
use chinook;
SELECT DISTINCT Country 
FROM customer;
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
/* SELECT DISTINCT [Cột / Cột AS Alias]
FROM   [Bảng dữ liệu]
WHERE  [Điều kiện lọc: AND, OR, NOT, LIKE, IS NULL, IN...]
ORDER BY [Cột sắp xếp ASC/DESC]
LIMIT  [Số dòng cần lấy]
OFFSET [Số dòng bỏ qua];   */
-- Nháp 1 (DISTINCT + Alias): Lấy danh sách tất cả các chức danh công việc (Title) duy nhất từ bảng employee. Đổi tên cột hiển thị thành Chuc_Vu.
select distinct Title as Chuc_vu from employee;
/* Nháp 2 (Phân trang LIMIT/OFFSET): 
Giả sử bạn đang làm giao diện danh sách hóa đơn. 
Hãy viết lệnh lấy dữ liệu cho Trang 3, biết mỗi trang chứa 5 hóa đơn (invoice), sắp xếp theo ngày lập hóa đơn InvoiceDate giảm dần.
*/
select InvoiceId,InvoiceDate,Total 
from invoice
order by InvoiceDate desc
limit 5;
/* Nháp 3 (LIKE + ORDER BY + Alias): 
Tìm các bài hát (track) chứa từ 'Rock' trong tên bài hát. 
Hiển thị 2 cột: tên bài hát đổi thành Ten_Bai_Hat, đơn giá đổi thành Gia_Tien. 
Sắp xếp bài hát theo giá giảm dần, nếu cùng giá thì xếp theo tên từ A-Z.
*/
select Name as Ten_Bai_Hat, UnitPrice as Gia_Tien
from track
where Name like '%Rock%'
order by UnitPrice desc, Name asc;
/* Nháp 4 (Tổng hợp đầy đủ các lệnh): 
Lấy danh sách các công ty (Company) khác NULL và không lặp lại của khách hàng ở nước 'USA'. 
Đổi tên cột thành Cong_Ty_Doi_Tac, sắp xếp theo tên công ty A-Z và lấy ra Top 3 công ty đầu tiên.
*/
select distinct company as Cong_Ty_Doi_Tac 
from customer
where company is not null and country = 'USA'
order by company asc 
limit 3;
/* Bài 1: 
Lấy ra danh sách tất cả các quốc gia (Country) duy nhất từ bảng customer. 
Đổi tên cột hiển thị thành Quoc_Gia và sắp xếp theo thứ tự từ A-Z.
*/
select distinct country as Quoc_Gia from customer 
order by country asc;
/* Bài 2: 
Tìm các bài hát (track) có tên (Name) chứa từ 'Love' (ở bất kỳ vị trí nào).
Hiển thị cột Name đổi tên thành Ten_Bai_Hat và Composer đổi tên thành Tac_Gia.
*/
select Name as Ten_Bai_Hat, Composer as Tac_Gia 
from track
where name like '%Love%';
/* Bài 3: 
Lấy thông tin khách hàng (customer) gồm FirstName, LastName, Email của những người dùng dịch vụ email của Yahoo (Email kết thúc bằng @yahoo.com).
*/
select FirstName,LastName,Email 
from customer
where Email like '%@yahoo.com';
/* Bài 4: 
Tìm tất cả các nhân viên (employee) có chức danh (Title) chứa từ 'Agent' VÀ báo cáo công việc cho quản lý (ReportsTo IS NOT NULL).
*/
select Title,FirstName,LastName 
from employee
where Title like '%Agent%' and ReportsTo is not null;
/* Bài 5: 
Lấy ra các hóa đơn (invoice) phát sinh tại nước 'USA' HOẶC 'Canada' VÀ có tổng tiền Total từ 5.00 đến 10.00 USD. 
Hiển thị InvoiceId, BillingCountry, Total.
*/
select InvoiceId, BillingCountry, Total 
from invoice 
where (BillingCountry = 'USA' or BillingCountry = 'Canada') and Total between 5 and 10; 
/*Bài 6: 
Tìm danh sách bài hát (track) có thời lượng Milliseconds lớn hơn 300,000 ms (~5 phút) nhưng thông tin tác giả Composer bị trống (IS NULL).
*/
select TrackId,Name,Milliseconds from track
where Milliseconds > 300000 and composer is null;
/* Bài 7 (Top N): 
Tìm Top 5 hóa đơn có giá trị lớn nhất (Total) trong bảng invoice. 
Hiển thị InvoiceId, CustomerId, Total (đổi tên thành Tong_Tien).
*/
select InvoiceId,CustomerId,Total as Tong_Tien 
from invoice
order by Total desc 
limit 5;
/*Bài 8 (Phân trang - Trang 2):
Giả sử giao diện hiển thị mỗi trang 10 khách hàng (customer), hãy viết câu lệnh lấy dữ liệu cho Trang 2 (sắp xếp theo CustomerId tăng dần).
*/
select CustomerId 
from customer
order by CustomerId asc
limit 10
offset 10;
/* Bài 9 (Phân trang - Trang 3): 
Viết câu lệnh lấy dữ liệu cho Trang 3 danh sách bài hát (track), biết mỗi trang chứa 8 bài hát, sắp xếp theo tên bài hát Name từ A-Z.
*/
select TrackId,Name 
from track
order by Name,TrackId asc 
limit 8
offset 16;
/*Bài 10 (Tổng hợp):
Lấy danh sách tên bài hát (Name đổi thành Ten_Bai), thời lượng (Milliseconds đổi thành Thoi_Gian) và đơn giá (UnitPrice đổi thành Gia_Ban) thỏa mãn:
Thuộc các loại MediaTypeId là 1 hoặc 2.
Đơn giá UnitPrice lớn hơn 0.99 USD.
Sắp xếp theo Đơn giá giảm dần, nếu giá bằng nhau thì sắp xếp theo Thời lượng tăng dần.
Chỉ lấy 6 kết quả đầu tiên.
*/
select Name as Ten_Bai, Milliseconds as Thoi_Gian, UnitPrice as Gia_Ban
from track
where MediaTypeId in (1,2) and UnitPrice > 0.99
order by UnitPrice desc, Milliseconds asc
limit 6; 
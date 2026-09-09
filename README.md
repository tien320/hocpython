# hocpython

Kho bài tập và project thực hành Python, SQL, Pandas và lập trình hướng đối
tượng. Repository hiện gồm các bài luyện cú pháp, cấu trúc dữ liệu, bài
LeetCode, xử lý dữ liệu Olist và một số ứng dụng CRUD nhỏ.

## Nội dung repository

### Bài tập Python

- `syntax1.py` đến `syntax9.py`: các bài luyện cú pháp Python.
- `luyensyntax.py`, `300baicode.py`, `test.py`: bài tập tổng hợp và thử nghiệm.
- `file_tong_hop.py`: file tổng hợp các bài thực hành.
- `lamsachchuoi.py`: bài tập xử lý và làm sạch chuỗi.
- `module1.py` đến `module4.py`: thực hành tách module và import module.
- `binarytree.py`, `linkedlist.py`: thực hành cây nhị phân và linked list.
- `leetcode/`: lời giải một số bài LeetCode và file review.

Tài liệu liên quan: [lithuyetpython.md](lithuyetpython.md),
[chiasyntax.md](chiasyntax.md) và [chiamodule.md](chiamodule.md).

### SQL và cơ sở dữ liệu

- `11-8.sql`, `crud.sql`, `crudnangcao.sql`: bài tập CRUD và truy vấn SQL.
- `cte-subquery.sql`, `sql-subquery.sql`: CTE, subquery và truy vấn lồng.
- `logs/query_log.sql`: log các câu truy vấn đã thực hành.
- `store.db`: cơ sở dữ liệu SQLite được dùng bởi một số project.
- `users.json`: dữ liệu mẫu dạng JSON.

Tài liệu tham khảo: [lithuyetsql.md](lithuyetsql.md) và
[pandas_crud_syntax_cheatsheet.md](pandas_crud_syntax_cheatsheet.md).

### Phân tích dữ liệu và ETL

- `hoc_pandas.py`: thực hành đọc, biến đổi và phân tích dữ liệu bằng Pandas.
- `readolist.py`: đọc và khám phá dữ liệu bộ Olist.
- `baitoanetl.py`: bài tập ETL.
- `pipeline.py`: pipeline đọc dữ liệu đơn hàng, làm sạch, join orders/items/products
  và tạo bảng doanh thu xuất kho theo ngày.
- `olist/`: các file CSV gốc của bộ dữ liệu Olist.
- `fact_outbound_daily.csv`: kết quả tổng hợp của pipeline ETL.
- `product_category_name_translation.csv`: dữ liệu dịch tên nhóm sản phẩm.
- `OLIST.png`: hình minh họa dữ liệu Olist.

### Các project ứng dụng

- [`project mathang/`](project%20mathang/): project Python hướng đối tượng về
  mặt hàng, đồ điện tử và tuổi thọ sản phẩm. Thư mục gồm `models/`, `schemas/`,
  `database/`, `api/`, `core/` và `main.py`.
- [`project1/`](project1/): ứng dụng quản lý sản phẩm và đơn hàng với SQLite,
  tổ chức theo các lớp database, model, repository, service và API trong `main.py`.
- [`project2/sinhvienmanage/`](project2/sinhvienmanage/): ứng dụng quản lý
  sinh viên gồm `sinhvien.py`, `repository.py`, `app.py` và `main.py`.
- [`project3/usermanage/`](project3/usermanage/): ứng dụng quản lý người dùng
  gồm `user.py`, `repository.py`, `app.py` và `main.py`.
- [`projectreview/studentmanagement/`](projectreview/studentmanagement/):
  project ôn tập quản lý sinh viên, có các lớp `Person`, `Student`, repository,
  app và main.

## Cách chạy

Tạo hoặc kích hoạt môi trường ảo trước khi chạy các project:

```powershell
\.venv\Scripts\Activate.ps1
```

Chạy một file bài tập ở thư mục gốc:

```powershell
python syntax1.py
python pipeline.py
```

Chạy project bằng cách chuyển tới đúng thư mục của project:

```powershell
cd project1
python main.py
```

Với project FastAPI trong `project mathang`, cần chạy lệnh từ chính thư mục
project để các import nội bộ hoạt động đúng:

```powershell
cd "project mathang"
python main.py
```

## Ghi chú

- Đây là repository học tập, nên các file có thể được bổ sung hoặc thay đổi
  thường xuyên.
- Các file SQL hiện có dùng cho việc học và thực hành truy vấn; repository chưa
  chứa cấu hình Oracle hoặc MongoDB.
- `pipeline.py` đang dùng đường dẫn dữ liệu được khai báo trực tiếp trong file.
  Khi chạy trên máy khác, cần cập nhật biến `DATA_FOLDER` cho phù hợp.

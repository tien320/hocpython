"""
Đề bài các bài tập ngày 1
Bài 1: Tính chỉ số khối cơ thể (BMI)Mục tiêu: Thực hành toán tử số học (/, **), ép kiểu dữ liệu float.Đề bài:Viết chương trình nhập vào chiều cao $h$ (tính bằng mét, ví dụ 1.75) và cân nặng $w$ (tính bằng kg, ví dụ 68.5).Tính chỉ số BMI theo công thức: $\text{BMI} = \frac{w}{h^2}$.In ra màn hình kết quả làm tròn đến 2 chữ số thập phân bằng hàm round().Ví dụ Output: Chỉ số BMI của bạn là: 22.37Bài 2: Tính toán tiền điện (Toán tử chia lấy dư và chia lấy nguyên)Mục tiêu: Thực hành chia lấy phần nguyên (//) và chia lấy phần dư (%).Đề bài:Nhập vào số phút sử dụng thiết bị điện (ví dụ: 135 phút).Đổi số phút này thành số giờ và số phút dư.Ví dụ: Input 135 $\rightarrow$ Output: 2 giờ và 15 phút.Bài 3: Trích xuất và định dạng tên (Xử lý chuỗi cơ bản)Mục tiêu: Thực hành các phương thức chuỗi: .strip(), .title(), .upper().Đề bài:Nhập vào tên của người dùng bị thừa khoảng trắng hai đầu và viết hoa/thường không chuẩn (Ví dụ: " ngUyEn vAn a ").Loại bỏ khoảng trắng thừa ở hai đầu.In tên dạng chuẩn danh xưng (In hoa chữ cái đầu mỗi từ): "Nguyen Van A".In tên dạng in hoa toàn bộ (dùng cho thẻ căn cước/hộ chiếu): "NGUYEN VAN A".Bài 4: Tạo email tự động từ họ tênMục tiêu: Nối chuỗi (+), ghép chuỗi và sử dụng phương thức .lower(), .replace().Đề bài:Nhập vào họ và tên không dấu (ví dụ: Nguyen Van An).Tạo địa chỉ email công ty theo quy tắc: <ten*khong_khoang_trang>@company.com (tất cả in thường).Ví dụ: Input "Nguyen Van An" $\rightarrow$ Output: nguyenvanan@company.com.Bài 5: Phân tích độ dài và ký tự của chuỗiMục tiêu: Dùng hàm len(), truy xuất ký tự qua chỉ số (Indexing).Đề bài:Nhập vào một câu bất kỳ từ bàn phím.In ra tổng số ký tự của câu đó.In ra ký tự đầu tiên và ký tự cuối cùng của câu.Ví dụ: Input "Python Rất Hay" $\rightarrow$ Độ dài: 14, Ký tự đầu: 'P', Ký tự cuối: 'y'.Bài 6: Đảo ngược và kiểm tra chuỗiMục tiêu: Thực hành Cắt chuỗi (Slicing [::-1]) và toán tử kiểm tra thành phần in.Đề bài:Nhập vào một chuỗi s. In ra chuỗi đảo ngược của s.Nhập một từ khóa k. Kiểm tra xem k có xuất hiện trong s hay không (trả về kiểu bool: True/False).Ví dụ:s = "Lập trình Python"Chuỗi đảo ngược: "nohtyP hnìrt pẠL"Kiểm tra "Python" in s $\rightarrow$ True.Bài 7: Lặp chuỗi tạo hình trang tríMục tiêu: Thực hành toán tử nhân chuỗi (*) và toán tử cộng chuỗi (+).Đề bài:Nhập vào một ký tự (ví dụ: \_) và một tiêu đề ngắn (ví dụ: THÔNG BÁO).In ra khung tiêu đề có dạng: **\*\*\***\*\*\*\***\*\*\***\* THÔNG BÁO **\*\*\*\***\*\*\***\*\*\*\*\*\*Sao cho viền sao ở hai bên có độ dài bằng nhau (ví dụ: mỗi bên 20 ký tự \*).Bài 8: Kiểm tra điều kiện điều kiện xét tuyển (Toán tử Boolean)Mục tiêu: Sử dụng toán tử so sánh (>, >=, ==) và toán tử logic (and, or, not) để trả về giá trị bool.Đề bài:Một thí sinh trúng tuyển nếu:Điểm Toán >= 5.0 AND Điểm Văn >= 5.0AND (Điểm trung bình (Toán + Văn + Anh) / 3 >= 6.5 OR có chứng chỉ Tiếng Anh has_certificate == True).Khai báo các biến điểm số và chứng chỉ bằng tay (hoặc input()), sau đó in ra kết quả ThuocDienTrungTuyen dạng True/False bằng duy nhất 1 biểu thức logic (chưa dùng lệnh if).Bài 9: Đảo ngược số có 3 chữ số (Toán tử số học)Mục tiêu: Kết hợp toán tử /, //, % để tách các chữ số hàng trăm, hàng chục, hàng đơn vị.Đề bài:Nhập vào một số nguyên có 3 chữ số (ví dụ: 457).Tách và tính tổng các chữ số: $4 + 5 + 7 = 16$.Tạo số đảo ngược từ số ban đầu: 754.Bài 10: Ứng dụng tính hóa đơn bán hàngMục tiêu: Tổng hợp biến, tính toán toán tử số học, ép kiểu và định dạng chuỗi (f-string).Đề bài:Viết chương trình nhập vào:Tên sản phẩm (str)Số lượng mua (int)Đơn giá (float)Tỷ lệ giảm giá (%) (float, ví dụ: 10 nghĩa là giảm 10%)Tính:Thành tiền = Số lượng $\times$ Đơn giáSố tiền giảm = Thành tiền $\times$ (Tỷ lệ giảm giá / 100)Tổng chi trả = Thành tiền - Số tiền giảmIn hóa đơn ra màn hình trình bày đẹp mắt bằng f-string.
"""

# Đề bài ngày 2

Bài 1: Lọc số chẵn và số lẻ
Mục tiêu: Duyệt mảng cơ bản và kiểm tra chia hết (%).

Đề bài:
Cho sẵn một danh sách các số nguyên: numbers = [12, 5, 8, 19, 24, 3, 7, 30].
Tạo hai danh sách mới: danh_sach_chan chứa các số chẵn và danh_sach_le chứa các số lẻ.

Output mong muốn:

Số chẵn: [12, 8, 24, 30]

Số lẻ: [5, 19, 3, 7]

# Đề bài - Bài tập Python

Tài liệu này liệt kê đề bài các bài tập theo ngày. Mỗi bài bao gồm mục tiêu, mô tả và ví dụ đầu vào/đầu ra.

---

## Ngày 1

### Bài 1 — Tính chỉ số khối cơ thể (BMI)

- Mục tiêu: thực hành toán tử số học, ép kiểu float.
- Yêu cầu: Nhập chiều cao `h` (m) và cân nặng `w` (kg). Tính

$$BMI = \dfrac{w}{h^2}$$

- In kết quả làm tròn 2 chữ số: `round(bmi, 2)`.

**Ví dụ:** Input `h=1.75`, `w=68.5` → Output: `Chỉ số BMI của bạn là: 22.37`.

### Bài 2 — Chia giờ/phút từ tổng phút

- Mục tiêu: thực hành `//` và `%`.
- Yêu cầu: Nhập số phút (ví dụ 135) → đổi sang `giờ` và `phút`.

```text
135 -> 2 giờ 15 phút
```

### Bài 3 — Chuỗi: strip/title/upper

- Mục tiêu: xử lý chuỗi `.strip()`, `.title()`, `.upper()`.
- Yêu cầu: Chuẩn hoá tên đầu vào (xóa khoảng trắng, in hoa chữ cái đầu mỗi từ, in hoa toàn bộ).

... (các bài khác tương tự)

---

## Ngày 2

### Bài 1 — Lọc số chẵn và số lẻ

- Mục tiêu: duyệt list và kiểm tra chia hết `%`.
- Yêu cầu: Từ `numbers = [12, 5, 8, 19, 24, 3, 7, 30]` tạo `chan` và `le`.

**Ví dụ:** `chan = [12, 8, 24, 30]`, `le = [5, 19, 3, 7]`.

### Bài 2 — Lọc số >= trung bình

- Mục tiêu: dùng `sum()` và `len()` để tính trung bình và lọc.
- Yêu cầu: Với `scores = [6.5, 8.0, 4.5, 9.0, 7.5, 5.0, 8.5]` in ra điểm trung bình và các điểm >= trung bình.

### Bài 3 — Tìm max/min không dùng hàm có sẵn

- Mục tiêu: luyện duyệt danh sách và cập nhật biến trạng thái.
- Yêu cầu: tìm `max_val` và `min_val` bằng vòng lặp.

### Bài 4 — Chuẩn hoá và lọc tên

- Mục tiêu: xử lý chuỗi, lọc theo độ dài.
- Yêu cầu: Loại bỏ khoảng trắng thừa, lọc tên có độ dài > 3.

### Bài 5 — Lọc phần tử duy nhất (giữ thứ tự)

- Mục tiêu: loại bỏ trùng lặp bằng kiểm tra `not in`.

### Bài 6 — Lọc số nguyên tố trong list

- Mục tiêu: vòng lặp + kiểm tra tính nguyên tố.

### Bài 7 — Tách dữ liệu hỗn hợp

- Mục tiêu: dùng `isinstance()` để lọc kiểu `int` (loại trừ `bool`).

### Bài 8 — Lọc sản phẩm theo giá (dict list)

- Mục tiêu: duyệt list chứa dict và lọc theo `price`.

```python
products = [
    {"name": "Laptop", "price": 15000000},
    {"name": "Chuột", "price": 250000},
    {"name": "Bàn phím", "price": 800000},
    {"name": "Tai nghe", "price": 450000},
    {"name": "Màn hình", "price": 3500000},
]
```

Lọc sản phẩm dưới `1_000_000` → `['Chuột', 'Bàn phím', 'Tai nghe']`.

---

Tệp này có thể mở rộng thêm ví dụ mẫu hoặc lời giải tham khảo cho từng bài khi cần.

    {"name": "Tai nghe", "price": 450000},
    {"name": "Màn hình", "price": 3500000},

]

```

Lọc sản phẩm dưới `1_000_000` → `['Chuột', 'Bàn phím', 'Tai nghe']`.

---

Tệp này có thể mở rộng thêm ví dụ mẫu hoặc lời giải tham khảo cho từng bài khi cần.
```

## Ngày 3

### Bài 1:

- Thao tác thêm, sửa, xóa trên List cơ bảnMục tiêu: Nắm vững .append(), .insert(), .remove(), .pop().Đề bài:Tạo danh sách todos = ["Học Python", "Đọc sách", "Tập thể dục"].Thêm công việc "Đi chợ" vào cuối danh sách.Chèn công việc "Uống nước" vào đầu danh sách (index 0).Xóa công việc "Đọc sách" khỏi danh sách.Lấy công việc cuối cùng ra khỏi danh sách và in công việc đó ra màn hình.

### Bài 2:

- Cắt lát (Slicing) danh sách nâng caoMục tiêu: Làm chủ cú pháp list[start:stop:step].Đề bài:Cho danh sách numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100].In ra 3 phần tử đầu tiên.In ra 4 phần tử cuối cùng.In ra danh sách chứa các phần tử ở vị trí index lẻ (1, 3, 5, ...).In ra danh sách đảo ngược của numbers.

### Bài 3:

- Tìm giá trị lớn thứ hai trong ListMục tiêu: Tư duy sắp xếp hoặc lọc phần tử lớn nhất.Đề bài:Cho mảng điểm số: scores = [85, 92, 78, 92, 88, 76, 90].Tìm và in ra giá trị lớn thứ hai trong danh sách (chú ý trường hợp có hai giá trị lớn nhất trùng nhau).Output mong muốn: 90

### Bài 4:

- Chuyển đổi và thao tác trên Tuple (Immutable Workaround)Mục tiêu: Hiểu bản chất không thể thay đổi của Tuple và cách chuyển đổi qua lại với List.Đề bài:Cho một Tuple chứa thông tin cố định: info = ("Nguyễn Văn A", 2002, "Ha Noi").Thử thay đổi năm sinh thành 2003 trực tiếp và quan sát lỗi báo về.Chuyển info sang kiểu List, cập nhật năm sinh thành 2003, thêm quê quán "Việt Nam" vào cuối, sau đó đóng gói lại thành Tuple mới.

### Bài 5:

- Tách danh sách thành các phần nhỏ (Chunking)Mục tiêu: Kết hợp range() và cắt lát slice trong vòng lặp.Đề bài:Cho một danh sách gồm 9 phần tử: data = [1, 2, 3, 4, 5, 6, 7, 8, 9].Chia danh sách này thành các danh sách con có độ dài $n = 3$.Output mong muốn: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

### Bài 6:

- Đảo ngược các chuỗi bên trong ListMục tiêu: Duyệt List và áp dụng slicing [::-1] cho từng phần tử chuỗi.Đề bài:Cho danh sách các từ: words = ["python", "developer", "data", "pipeline"].Tạo một danh sách mới chứa các từ đã bị đảo ngược ký tự.Output mong muốn: ['nohtyp', 'repoleved', 'atad', 'enilepip']

### Bài 7:

- Gộp hai List và loại bỏ trùng lặp giữ nguyên thứ tựMục tiêu: Nắm vững .extend() hoặc toán tử + kết hợp kiểm tra not in.Đề bài:Cho hai danh sách:list1 = [1, 3, 5, 7, 9]list2 = [3, 4, 5, 6, 7]Gộp hai danh sách trên thành một danh sách duy nhất chỉ chứa các phần tử không trùng lặp và giữ đúng thứ tự xuất hiện.Output mong muốn: [1, 3, 5, 7, 9, 4, 6]

### Bài 8:

- Đóng gói và Mở gói Tuple (Tuple Packing & Unpacking)Mục tiêu: Thực hành kỹ thuật Unpacking dữ liệu rất phổ biến trong Python.Đề bài:Cho một Tuple chứa tọa độ và thông tin điểm: record = ("P1", (10.5, 20.0), "Active").Mở gói record ra 3 biến: point_name, coordinates, status.Tiếp tục mở gói biến coordinates ra 2 biến tọa độ x và y.In ra thông tin dạng: Điểm P1 tại vị trí X=10.5, Y=20.0 đang ở trạng thái Active.

### Bài 9:

- Xóa tất cả các phần tử trùng lặp đứng liền kềMục tiêu: Duyệt List với chỉ số index để so sánh phần tử hiện tại và phần tử trước đó.Đề bài:Cho danh sách bị lặp liên tiếp: nums = [1, 1, 2, 3, 3, 3, 2, 4, 4, 1].Rút gọn danh sách sao cho các phần tử giống nhau đứng cạnh nhau chỉ giữ lại 1 đại diện.Output mong muốn: [1, 2, 3, 2, 4, 1]

### Bài 10:

- Xoay vòng List (Rotate List)Mục tiêu: Ứng dụng cắt lát (slicing) và ghép danh sách (+).Đề bài:Cho danh sách arr = [1, 2, 3, 4, 5, 6, 7] và số nguyên $k = 3$.Hãy xoay vòng danh sách sang phải $k$ bước (các phần tử ở cuối dịch chuyển lên đầu).Giải thích: Xoay 1 bước: [7, 1, 2, 3, 4, 5, 6] $\rightarrow$ Xoay 3 bước: [5, 6, 7, 1, 2, 3, 4].Output mong muốn: [5, 6, 7, 1, 2, 3, 4]

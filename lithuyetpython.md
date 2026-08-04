# Kiến thức lý thuyết Python

## PHẦN 1: Kiểu dữ liệu nguyên thủy, Biến và Toán tử

### 1. Kiểu dữ liệu nguyên thủy (Primitive Data Types)

- `int` (Số nguyên): không có dấu thập phân.
  - Ví dụ: `-5`, `0`, `100`.
- `float` (Số thực): có dấu thập phân.
  - Ví dụ: `3.14`, `-0.5`, `2.0`.
- `str` (Chuỗi ký tự): đặt trong dấu nháy đơn hoặc đôi.
  - Ví dụ: `"Python"`, `'123'`.
- `bool` (Boolean): chỉ có hai giá trị `True` và `False`.
  - `True` tương ứng với giá trị đúng, `False` tương ứng với sai.

💡 Ép kiểu (Type Casting):

- `int("123")` → `123`
- `str(456)` → `"456"`
- `float(5)` → `5.0`

### 2. Biến (Variables)

- Biến dùng để lưu trữ dữ liệu trong bộ nhớ.
- Cú pháp: `ten_bien = gia_tri`
  - Ví dụ: `age = 20`, `name = "An"`.
- Quy tắc đặt tên:
  - Không bắt đầu bằng số.
  - Không chứa ký tự đặc biệt (ngoại trừ `_`).
  - Không trùng với từ khóa hệ thống như `if`, `for`, `class`.

### 3. Toán tử (Operators)

| Loại toán tử         | Ký hiệu                          | Ý nghĩa                                                            | Ví dụ (`a = 10`, `b = 3`)                                                               |
| -------------------- | -------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Số học               | `+`, `-`, `*`, `/`               | Cộng, Trừ, Nhân, Chia thực                                         | `10 / 3` → `3.3333...`                                                                  |
| Chia lấy phần nguyên | `//`                             | Chia và lấy phần nguyên                                            | `10 // 3` → `3`                                                                         |
| Chia lấy phần dư     | `%`                              | Lấy phần dư                                                        | `10 % 3` → `1`                                                                          |
| Lũy thừa             | `**`                             | Mũ                                                                 | `10 ** 3` → `1000`                                                                      |
| So sánh              | `==`, `!=`, `>`, `<`, `>=`, `<=` | Bằng, khác, lớn hơn, nhỏ hơn, lớn hơn hoặc bằng, nhỏ hơn hoặc bằng | `10 == 3` → `False`, `10 >= 3` → `True`                                                 |
| Logic                | `and`, `or`, `not`               | Kết hợp điều kiện                                                  | `(5 > 2) and (3 < 1)` → `False`; `(5 > 2) or (3 < 1)` → `True`; `not (5 > 2)` → `False` |
| Thành phần           | `in`, `not in`                   | Kiểm tra tồn tại trong chuỗi hoặc danh sách                        | `'a' in 'cat'` → `True`                                                                 |

## PHẦN 2: Cấu trúc điều kiện và Vòng lặp

### 1. Cấu trúc điều kiện (`if` - `elif` - `else`)

- Dùng để phân nhánh luồng thực thi dựa trên điều kiện đúng/sai.
- Luôn đặt dấu hai chấm `:` sau điều kiện và thụt lề 4 khoảng trắng cho khối lệnh bên trong.

```python
score = 8.5

if score >= 9.0:
    print("Xuất sắc")
elif score >= 8.0:
    print("Giỏi")  # Thực thi nhánh này và bỏ qua toàn bộ phần sau
else:
    print("Trung bình/Khá")
```

### 2. Vòng lặp `for`

- Dùng để lặp qua từng phần tử trong một chuỗi, danh sách hoặc dãy số `range()`.
- `range(5)` → `0, 1, 2, 3, 4` (5 lần).
- `range(2, 6)` → `2, 3, 4, 5`.
- `range(1, 10, 2)` → `1, 3, 5, 7, 9`.

```python
# Lặp duyệt qua phần tử danh sách
for item in ["táo", "cam", "xoài"]:
    print(item)
```

### 3. Vòng lặp `while`

- Thực thi khối lệnh chừng nào điều kiện còn `True`.
- Dùng khi chưa biết chính xác số lần lặp.

```python
count = 1
while count <= 3:
    print(f"Lần lặp {count}")
    count += 1  # Bắt buộc phải tăng biến đếm để tránh lặp vô tận
```

### 4. Lệnh điều khiển vòng lặp

- `break`: dừng và thoát ngay lập tức khỏi vòng lặp.
- `continue`: bỏ qua phần còn lại của lần lặp hiện tại, chuyển sang lần lặp tiếp theo.
- `pass`: giữ chỗ, không làm gì cả.

## PHẦN 3: Cấu trúc dữ liệu List và Tuple

### 1. So sánh List vs Tuple

| Tiêu chí           | List (Danh sách)                             | Tuple (Bộ dữ liệu)                             |
| ------------------ | -------------------------------------------- | ---------------------------------------------- |
| Cú pháp            | Dấu ngoặc vuông: `[1, 2, 3]`                 | Dấu ngoặc đơn: `(1, 2, 3)`                     |
| Tính chất          | Mutable (có thể thêm, sửa, xóa)              | Immutable (không thể sửa đổi sau khi tạo)      |
| Hiệu năng & bộ nhớ | Chiếm nhiều RAM hơn, truy xuất chậm hơn      | Nhẹ hơn, tối ưu bộ nhớ, truy xuất nhanh hơn    |
| Mục đích           | Dữ liệu biến động (giỏ hàng, danh sách động) | Dữ liệu cố định (tọa độ GPS, hằng số cấu hình) |

### 2. Truy cập và cắt lát (`Indexing` & `Slicing`)

- Áp dụng giống nhau cho List, Tuple và String.
- Chỉ số bắt đầu từ `0`; `-1` là phần tử cuối cùng.
- Cú pháp slicing: `sequence[start:stop:step]` (không lấy phần tử tại vị trí `stop`).

```python
data = [10, 20, 30, 40, 50, 60]

print(data[0])   # 10
print(data[-1])  # 60
print(data[1:4]) # [20, 30, 40] (lấy từ index 1 đến 3)
print(data[::2]) # [10, 30, 50] (nhảy bước 2)
print(data[::-1])# [60, 50, 40, 30, 20, 10] (đảo ngược danh sách)
```

### 3. Các hàm & phương thức tra cứu nhanh (List)

- Thêm phần tử:
  - `list.append(x)` → thêm `x` vào cuối list.
  - `list.insert(i, x)` → chèn `x` vào vị trí `i`.
  - `list.extend(iterable)` → nối thêm một iterable khác vào cuối.
- Xóa phần tử:
  - `list.pop(i)` → xóa và trả về phần tử tại index `i` (mặc định là phần tử cuối).
  - `list.remove(x)` → xóa phần tử đầu tiên có giá trị `x`.
  - `del list[i]` → dùng từ khóa `del` xóa phần tử tại index `i`.
  - `list.clear()` → xóa sạch danh sách về `[]`.
- Tìm kiếm & sắp xếp:
  - `len(list)` → đếm tổng số phần tử.
  - `list.sort()` → sắp xếp trực tiếp trên list gốc.
  - `sorted(iterable)` → trả về list mới đã sắp xếp, không làm thay đổi list gốc.
  - `list.count(x)` → đếm số lần `x` xuất hiện.
  - `list.index(x)` → trả về vị trí index đầu tiên của `x`.

## PHẦN 4: Dictionary và Set

### 1. Dictionary (Từ điển - Map / Key-Value)

Dictionary lưu trữ dữ liệu dưới dạng Cặp khóa - giá trị (Key - Value).

Key (Khóa): Phải là duy nhất (Unique) và thuộc kiểu Immutable (như int, str, tuple).

Value (Giá trị): Có thể là bất kỳ kiểu dữ liệu nào (kể cả list, dict khác) và cho phép trùng lặp.

Từ Python 3.7+, dict có đặc tính giữ nguyên thứ tự (Ordered) theo thời điểm thêm vào.
A. Cú pháp & Khởi tạo

student = {
"id": 101,
"name": "Nguyễn Văn A",
"scores": [8.5, 9.0, 7.5]
}
B. Truy cập & Thêm / Sửa / Xóa

- 1. Truy cập
     print(student["name"]) # 'Nguyễn Văn A' (Báo lỗi KeyError nếu Key không tồn tại)
     print(student.get("age", 20)) # 20 (Dùng .get() an toàn: trả về 20 nếu không thấy key "age")

- 2. Thêm hoặc Sửa
     student["age"] = 22 # Thêm key "age" mới với giá trị 22
     student["name"] = "Nguyễn An" # Sửa giá trị của key "name" hiện có

- 3. Xóa
     del student["scores"] # Xóa key "scores"
     age = student.pop("age") # Xóa key "age" và trả về giá trị của nó

C. Duyệt qua Dictionary
data = {"a": 1, "b": 2, "c": 3}

for key in data.keys(): # Duyệt các Key
print(key)

for val in data.values(): # Duyệt các Value
print(val)

for key, val in data.items(): # Duyệt cả Key và Value (RẤT HAY DÙNG)
print(f"Key: {key} -> Value: {val}")

### 2. Set (Tập hợp - HashSet)

Set là một tập hợp không có thứ tự (Unordered) và chỉ chứa các phần tử duy nhất (No Duplicates).

Mọi phần tử trong Set bắt buộc phải là kiểu Immutable (int, float, str, tuple).
A. Cú pháp & Khởi tạo
numbers = {1, 2, 3, 4, 3, 2} # Tự động lọc trùng -> {1, 2, 3, 4}
empty_set = set() # ⚠️ Lưu ý: {} tạo ra dict rỗng, muốn tạo set rỗng phải dùng set()
B. Thêm & Xóa phần tử
s = {1, 2, 3}

s.add(4) # Thêm 1 phần tử -> {1, 2, 3, 4}
s.remove(2) # Xóa số 2 (Báo lỗi KeyError nếu 2 không tồn tại)
s.discard(10) # Xóa số 10 (Không báo lỗi nếu 10 không tồn tại - An toàn hơn)
C. Các phép toán tập hợp (Set Operations)
Đây là điểm mạnh nhất của Set, cực kỳ hữu ích khi làm bài tập logic/dữ liệu:
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A | B) # Phép Hợp (Union): {1, 2, 3, 4, 5, 6} - lấy tất cả
print(A & B) # Phép Giao (Intersection): {3, 4} - lấy phần chung
print(A - B) # Phép Hiệu (Difference): {1, 2} - thuộc A nhưng không thuộc B
print(A ^ B) # Phép Hiệu đối xứng: {1, 2, 5, 6} - phần tử không chung

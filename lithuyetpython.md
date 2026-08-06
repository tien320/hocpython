# Python Full Fundamentals Cheatsheet for DSA

Bao gồm: Kiểu dữ liệu nguyên thủy, Biến, Toán tử, Chuỗi, Điều kiện, Vòng lặp, List, Tuple, Set, Dictionary và List of Dicts (Mô phỏng Bảng dữ liệu).

---

## 1. Kiểu dữ liệu nguyên thủy, Biến & Toán tử

```python
# --- A. KIỂU DỮ LIỆU NGUYÊN THỦY ---
x = 10          # int: Số nguyên
y = 3.14        # float: Số thực
name = "Python" # str: Chuỗi ký tự
is_valid = True # bool: Đúng/Sai (True/False)

# --- B. TOÁN TỬ SỐ HỌC ---
add = 10 + 3    # 13  : Cộng
sub = 10 - 3    # 7   : Trừ
mul = 10 * 3    # 30  : Nhân
div = 10 / 3    # 3.333... : Chia số thực
div_floor = 10 // 3 # 3 : Chia lấy phần nguyên (Rất quan trọng cho DSA/Binary Search)
mod = 10 % 3    # 1   : Chia lấy phần dư
pow_val = 2 ** 3 # 8  : Lũy thừa 2^3

# --- C. TOÁN TỬ SO SÁNH & LOGIC ---
res1 = (10 > 3) and (5 == 5) # True (Cả 2 đều đúng)
res2 = (10 < 3) or (5 == 5)  # True (Chỉ cần 1 cái đúng)
res3 = not (10 == 3)        # True (Đảo ngược giá trị)

```

s = " Data Structure "

# --- A. BIẾN ĐỔI CHUỖI ---

s_clean = s.strip() # "Data Structure" : Xóa khoảng trắng 2 đầu
s_upper = s.upper() # " DATA STRUCTURE " : Viết hoa toàn bộ
s_lower = s.lower() # " data structure " : Viết thường toàn bộ
s_rep = s.replace("Data", "Algorithm") # Thay thế từ "Data" -> "Algorithm"

# --- B. CẮT & TÁCH CHUỖI ---

words = "a,b,c".split(",") # ['a', 'b', 'c'] : Tách chuỗi thành List dựa vào dấu phẩy
joined = "-".join(words) # "a-b-c" : Nối List thành chuỗi bằng ký tự nối

# --- C. SLICING & FORMATTING ---

sub_str = s_clean[0:4] # "Data" : Cắt từ index 0 đến 3
rev_str = s_clean[::-1] # "erutcurtS ataD" : Đảo ngược chuỗi bằng slicing
formatted = f"Name: {s_clean}, Length: {len(s_clean)}" # f-string format

# --- A. IF - ELIF - ELSE ---

score = 85
if score >= 90:
grade = 'A'
elif score >= 80:
grade = 'B' # Chạy nhánh này
else:
grade = 'C'

# --- B. VÒNG LẶP FOR ---

for i in range(5): # Lặp từ 0 đến 4
pass

for i in range(1, 10, 2): # Lặp từ 1 đến 9, bước nhảy 2 (1, 3, 5, 7, 9)
pass

# Duyệt lấy cả index và giá trị bằng enumerate()

arr = ["a", "b", "c"]
for idx, val in enumerate(arr):
print(idx, val) # 0 'a', 1 'b', 2 'c'

# --- C. VÒNG LẶP WHILE ---

count = 3
while count > 0:
count -= 1 # Giảm dần điều kiện dừng
if count == 1:
break # Thoát vòng lặp ngay lập tức

# --- A. LIST (Có thể sửa đổi - Mutable) ---

lst = [10, 20, 30, 40]

# Truy cập & Slicing

first = lst[0] # 10 : Phần tử đầu
last = lst[-1] # 40 : Phần tử cuối
sub_lst = lst[1:3] # [20, 30] : Cắt từ index 1 đến 2

# Thêm / Sửa / Xóa

lst.append(50) # [10, 20, 30, 40, 50] - O(1): Thêm vào cuối
lst.insert(1, 15) # [10, 15, 20, 30, 40, 50] - O(n): Chèn vào vị trí 1
lst[0] = 99 # [99, 15, 20, 30, 40, 50] : Sửa giá trị
val = lst.pop() # 50 (xóa cuối - O(1))
val_idx = lst.pop(1) # 15 (xóa vị trí index 1 - O(n))
lst.remove(20) # Xóa phần tử có giá trị 20 đầu tiên tìm thấy - O(n)

# --- B. TUPLE (Không thể sửa đổi - Immutable) ---

point = (10, 20) # Khai báo bằng ngoặc đơn ()
x, y = point # Unpacking tuple: x = 10, y = 20

# --- A. SET (Duy nhất, không thứ tự, Tìm kiếm O(1)) ---

s = {1, 2, 3}
s.add(4) # Thêm phần tử
s.add(2) # Bị bỏ qua vì 2 đã tồn tại
s.remove(1) # Xóa phần tử 1
is_exist = 3 in s # True - Kiểm tra sự tồn tại mất O(1)

# --- B. DICTIONARY (Cặp Key-Value, Tìm kiếm O(1)) ---

d = {"name": "Alice", "age": 20}
d["score"] = 9.5 # Thêm/Sửa key-value
age = d.get("age", 0) # 20 : Lấy an toàn, nếu không có trả về 0
del d["score"] # Xóa key "score"

# Duyệt qua Dictionary

for key, value in d.items():
print(key, value)

# Danh sách chứa các đối tượng sinh viên

students = [
{"id": 1, "name": "Alice", "score": 8.5, "active": True},
{"id": 2, "name": "Bob", "score": 4.0, "active": True},
{"id": 3, "name": "Charlie", "score": 9.0, "active": False}
]

# 1. Lọc các sinh viên active có score >= 5.0 (Filtering)

passed_students = [
s for s in students
if s["active"] and s["score"] >= 5.0
]

# Result: [{'id': 1, 'name': 'Alice', 'score': 8.5, 'active': True}]

# 2. Lấy danh sách tất cả tên sinh viên (Projection/Mapping)

student_names = [s["name"] for s in students]

# Result: ['Alice', 'Bob', 'Charlie']

# 3. Tìm sinh viên theo ID (Lookup O(n) trên List)

def find_by_id(data, target_id):
for item in data:
if item["id"] == target_id:
return item
return None

# 4. Cập nhật dữ liệu hàng loạt (Update)

for s in students:
if s["score"] < 5.0:
s["status"] = "Failed"
else:
s["status"] = "Passed"

# Python Fundamentals & DSA Basics Cheat Sheet

Lý thuyết cốt lõi về Hàm (Function), Tham số nâng cao (`*args`, `**kwargs`), Đệ quy và các Cấu trúc dữ liệu nền tảng cho Thuật toán.

---

## 1. Khai báo Hàm & Giá trị trả về (`return`)

```python
# 1. Hàm cơ bản: có nhận tham số và trả về giá trị
def add(a: int, b: int) -> int:
    return a + b  # 'return' trả về kết quả và THOÁT hàm ngay lập tức

# 2. Hàm trả về nhiều giá trị (dưới dạng Tuple)
def get_min_max(numbers: list):
    return min(numbers), max(numbers)  # Trả về một tuple (min, max)

low, high = get_min_max([5, 2, 9, 1])  # Tuple Unpacking: low=1, high=9
```

# 1. \*args: Nhận số lượng tham số vị trí TÙY Ý (lưu dưới dạng Tuple)

def sum_all(\*args): # args = (1, 2, 3, 4)
return sum(args) # Duyệt hoặc dùng hàm built-in trên tuple 'args'

# 2. \*\*kwargs: Nhận số lượng tham số có tên TÙY Ý (lưu dưới dạng Dictionary)

def print_profile(\*\*kwargs): # kwargs = {'name': 'Alice', 'age': 20}
for key, value in kwargs.items():
print(f"{key}: {value}")

# 3. Thứ tự tham số bắt buộc khi phối hợp: Standard -> \*args -> Default -> \*\*kwargs

def full_func(req_1, req_2, \*args, default_param=100, \*\*kwargs):
pass # 'pass' là keyword giữ vị trí khi chưa viết logic

# --- A. LIST (Mảng động) ---

arr = [1, 2, 3]
arr.append(4) # O(1) - Thêm vào cuối
val = arr.pop() # O(1) - Lấy & xóa phần tử cuối
first = arr[0] # O(1) - Truy cập ngẫu nhiên qua index
sub = arr[1:3] # O(k) - Slice mảng (k là độ dài sublist)

# --- B. SET (Tập hợp - Giá trị duy nhất, Không thứ tự) ---

my_set = {1, 2, 3}
my_set.add(4) # O(1) trung bình - Thêm phần tử
if 2 in my_set: pass # O(1) trung bình - Tìm kiếm cực nhanh

# --- C. DICTIONARY (Bảng băm Key-Value) ---

lookup = {"a": 1, "b": 2}
lookup["c"] = 3 # O(1) trung bình - Thêm / Cập nhật
val = lookup.get("a") # O(1) trung bình - Truy xuất giá trị an toàn

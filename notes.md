# Ghi chú nhanh về Python (các khái niệm cơ bản)

## 1. Cấu trúc điều kiện

Cấu trúc điều kiện cho phép chương trình đưa ra quyết định — chỉ thực thi một khối lệnh khi điều kiện trả về `True`.

- Lưu ý: Python dùng indentation (thụt lề) để xác định khối lệnh (thường 4 khoảng trắng).

Ví dụ:

```python
tuoi = 18
if tuoi >= 18:
	print("Bạn đã đủ tuổi bầu cử!")

so = 7
if so % 2 == 0:
	print("Đây là số chẵn.")
else:
	print("Đây là số lẻ.")

diem = 7.5
if diem >= 8.5:
	print("Xếp loại: Giỏi")
elif diem >= 7.0:
	print("Xếp loại: Khá")
elif diem >= 5.0:
	print("Xếp loại: Trung bình")
else:
	print("Xếp loại: Yếu")
```

## 2. Vòng lặp `for`

Vòng lặp `for` dùng để duyệt qua một chuỗi hoặc danh sách.

```python
ten = "Python"
for ky_tu in ten:
	print(ky_tu)

for i in range(5):
	print(f"Lần lặp thứ {i}")

for i in range(2, 11, 2):
	print(i, end=" ")  # Output: 2 4 6 8 10
```

## 3. Vòng lặp `while`

`while` lặp chừng nào điều kiện còn đúng. Luôn đảm bảo điều kiện sẽ trở thành `False` để tránh vòng lặp vô hạn.

```python
dem = 1
while dem <= 5:
	print(f"Số hiện tại: {dem}")
	dem += 1
```

## 4. Điều khiển vòng lặp: `break`, `continue`, `pass`

- `break`: thoát vòng lặp ngay lập tức.
- `continue`: bỏ qua phần còn lại của lần lặp hiện tại.
- `pass`: giữ chỗ, không làm gì (dùng khi muốn để khối trống).

Ví dụ:

```python
for i in range(1, 21):
	if i % 7 == 0:
		print(f"Tìm thấy số đầu tiên chia hết cho 7 là: {i}")
		break

for i in range(1, 6):
	if i == 3:
		continue
	print(i)
```

## 5. Toán tử logic

- `and`: trả về `True` nếu cả hai biểu thức đều đúng.
- `or`: trả về `True` nếu một trong các biểu thức đúng.
- `not`: đảo giá trị boolean.

## 6. Một số phương thức danh sách (list)

- `append(x)`: thêm phần tử vào cuối danh sách.
- `clear()`: xóa toàn bộ phần tử.
- `copy()`: trả về bản sao của danh sách.
- `count(x)`: đếm số lần xuất hiện của giá trị.
- `extend(iterable)`: nối thêm các phần tử từ iterable.
- `index(x)`: trả về chỉ số xuất hiện đầu tiên của giá trị.
- `insert(i, x)`: chèn `x` vào vị trí `i`.
- `pop(i)`: xóa phần tử tại chỉ số `i` (mặc định là cuối danh sách).
- `remove(x)`: xóa phần tử đầu tiên có giá trị `x`.
- `reverse()`: đảo ngược thứ tự phần tử.
- `sort()`: sắp xếp danh sách (thay đổi tại chỗ).

---

Ghi chú: Tài liệu này là bản tóm tắt nhanh; khi cần, có thể thêm ví dụ chi tiết cho mỗi mục.

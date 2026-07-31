"""
Bài 10: Ứng dụng tính hóa đơn bán hàng
Mục tiêu: Tổng hợp biến, tính toán toán tử số học, ép kiểu và định dạng chuỗi (f-string).
Đề bài:
Viết chương trình nhập vào:
Tên sản phẩm (str)
Số lượng mua (int)
Đơn giá (float)
Tỷ lệ giảm giá (%) (float, ví dụ: 10 nghĩa là giảm 10%)
Tính:
Thành tiền = Số lượng $\times$ Đơn giá
Số tiền giảm = Thành tiền $\times$ (Tỷ lệ giảm giá / 100)
Tổng chi trả = Thành tiền - Số tiền giảm
In hóa đơn ra màn hình trình bày đẹp mắt bằng f-string.
"""


product_name = input("Nhập tên sản phẩm: ")
quantity = int(input("Nhập số lượng mua: "))
unit_price = float(input("Nhập đơn giá: "))
discount_rate = float(input("Nhập tỷ lệ giảm giá (%): "))

total_amount = quantity * unit_price
discount_amount = total_amount * (discount_rate / 100)
total_payment = total_amount - discount_amount

print(f"\nHóa đơn bán hàng")
print(f"Tên sản phẩm: {product_name}")
print(f"Số lượng: {quantity}")
print(f"Đơn giá: {unit_price:.2f}")
print(f"Tỷ lệ giảm giá: {discount_rate}%")
print(f"Thành tiền: {total_amount:.2f}")
print(f"Số tiền giảm: {discount_amount:.2f}")
print(f"Tổng chi trả: {total_payment:.2f}")
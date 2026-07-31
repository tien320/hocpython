"""
Bài 2: Tính toán tiền điện (Toán tử chia lấy dư và chia lấy nguyên)
Mục tiêu: Thực hành chia lấy phần nguyên (//) và chia lấy phần dư (%).
Đề bài:
Nhập vào số phút sử dụng thiết bị điện (ví dụ: 135 phút).
Đổi số phút này thành số giờ và số phút dư.
Ví dụ: Input 135 $\rightarrow$ Output: 2 giờ và 15 phút.
"""


minutes = int(input())  # Nhập số phút sử dụng thiết bị điện
hours = minutes // 60 # Tính số giờ bằng cách chia lấy phần nguyên
remaining_minutes = minutes % 60 # Tính số phút dư
print(f"{hours} giờ và {remaining_minutes} phút")
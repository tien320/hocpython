"""
Bài 7: Lặp chuỗi tạo hình trang trí
Mục tiêu: Thực hành toán tử nhân chuỗi (*) và toán tử cộng chuỗi (+).
Đề bài:
Nhập vào một ký tự (ví dụ: *) và một tiêu đề ngắn (ví dụ: THÔNG BÁO).
In ra khung tiêu đề có dạng: ******************* THÔNG BÁO *******************
Sao cho viền sao ở hai bên có độ dài bằng nhau (ví dụ: mỗi bên 20 ký tự *).
"""

char = input()  # Nhập ký tự
title = input()  # Nhập tiêu đề
border_length = 20  # Độ dài viền
border = char * border_length  # Tạo viền
print(f"{border} {title} {border}")  # In khung tiêu đề
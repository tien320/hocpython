"""
Bài 4: Tạo email tự động từ họ tên
Mục tiêu: Nối chuỗi (+), ghép chuỗi và sử dụng phương thức .lower(), .replace().
Đề bài:Nhập vào họ và tên không dấu (ví dụ: Nguyen Van An).
Tạo địa chỉ email công ty theo quy tắc: <ten_khong_khoang_trang>@company.com (tất cả in thường).
Ví dụ: Input "Nguyen Van An" 
       Output: nguyenvanan@company.com.
"""

name = input()  # Nhập họ và tên không dấu
email = name.replace(" ", "").lower() + "@company.com"  # Tạo email
print(email)  # In địa chỉ email
"""
Bài 3: Trích xuất và định dạng tên (Xử lý chuỗi cơ bản)
Mục tiêu: Thực hành các phương thức chuỗi: .strip(), .title(), .upper().
Đề bài:
Nhập vào tên của người dùng bị thừa khoảng trắng hai đầu và viết hoa/thường không chuẩn (Ví dụ: "  ngUyEn vAn a  ").
Loại bỏ khoảng trắng thừa ở hai đầu.
In tên dạng chuẩn danh xưng (In hoa chữ cái đầu mỗi từ): "Nguyen Van A".
In tên dạng in hoa toàn bộ (dùng cho thẻ căn cước/hộ chiếu): "NGUYEN VAN A".
"""

name = input()  # Nhập tên người dùng
name = name.strip()  # Loại bỏ khoảng trắng thừa ở hai đầu
name = name.title()  # In hoa chữ cái đầu mỗi từ
print(name)  # In tên dạng chuẩn danh xưng
print(name.upper())  # In tên dạng in hoa toàn bộ
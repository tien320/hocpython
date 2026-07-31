"""
Bài 5: Kiểm tra chuỗi đối xứng
Mục tiêu: Sử dụng slicing và các phương thức chuỗi để kiểm tra chuỗi đối xứng.
Đề bài:
Nhập vào một chuỗi (không chứa khoảng trắng).
Kiểm tra xem chuỗi có phải là chuỗi đối xứng không (ví dụ: "racecar", "level").
In kết quả: "Đây là chuỗi đối xứng" hoặc "Đây không phải là chuỗi đối xứng".
"""


string = input()  # Nhập chuỗi
string = string.replace(" ", "").lower()  # Loại bỏ khoảng trắng và chuyển về chữ thường
reversed_string = string[::-1]  # Đảo ngược chuỗi
if string == reversed_string:
    print("Đây là chuỗi đối xứng")
else:
    print("Đây không phải là chuỗi đối xứng")
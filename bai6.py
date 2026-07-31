"""
Bài 6: Đếm số lần xuất hiện của một ký tự trong chuỗi
Mục tiêu: Sử dụng phương thức .count() để đếm số lần xuất hiện của một ký tự trong chuỗi.
Đề bài:
Nhập vào một chuỗi và một ký tự.
Đếm số lần xuất hiện của ký tự đó trong chuỗi.
In kết quả.
"""


string = input()  # Nhập chuỗi
char = input()  # Nhập ký tự
count = string.count(char)  # Đếm số lần xuất hiện của ký tự
print(count)  # In kết quả
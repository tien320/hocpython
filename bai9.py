"""
Bài 9: Đảo ngược số có 3 chữ số (Toán tử số học)
Mục tiêu: Kết hợp toán tử /, //, % để tách các chữ số hàng trăm, hàng chục, hàng đơn vị.
Đề bài:
Nhập vào một số nguyên có 3 chữ số (ví dụ: 123).
Tách các chữ số hàng trăm, hàng chục, hàng đơn vị.
In ra số đảo ngược (ví dụ: 321).
"""

number = int(input())  # Nhập số nguyên có 3 chữ số
hundreds = number // 100  # Tách chữ số hàng trăm
tens = (number // 10) % 10  # Tách chữ số hàng chục
units = number % 10  # Tách chữ số hàng đơn vị  
reversed_number = units * 100 + tens * 10 + hundreds  # Tạo số đảo ngược
print(reversed_number)  # In ra số đảo ngược

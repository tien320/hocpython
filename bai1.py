""""
Bài 1: Tính chỉ số khối cơ thể (BMI)
Mục tiêu: Thực hành toán tử số học (/, **), ép kiểu dữ liệu float.
 Đề bài:Viết chương trình nhập vào chiều cao(tính bằng mét, ví dụ 1.75) và cân nặng (tính bằng kg, ví dụ 68.5).
   Tính chỉ số BMI theo công thức: bmi = cân nặng / (chiều cao ** 2)
   In ra màn hình kết quả làm tròn đến 2 chữ số thập phân 
   bằng hàm round().
   Ví dụ Output: Chỉ số BMI của bạn là: 22.37
"""
can_nang = float(input()) #tinh theo kg
chieu_cao = float(input()) #tinh theo m
bmi = can_nang / (chieu_cao ** 2)
print(bmi)
"""
Bài 8: Kiểm tra điều kiện xét tuyển (Toán tử Boolean)
Mục tiêu: Sử dụng toán tử so sánh (>, >=, ==) 
và toán tử logic (and, or, not) để trả về giá trị bool.

Đề bài:
Một thí sinh trúng tuyển nếu:

Điểm Toán >= 5.0 AND Điểm Văn >= 5.0

AND (Điểm trung bình (Toán + Văn + Anh) / 3 >= 6.5 OR có chứng chỉ Tiếng Anh has_certificate == True).

Khai báo các biến điểm số và chứng chỉ bằng tay (hoặc input()), sau đó in ra kết quả ThuocDienTrungTuyen dạng True/False bằng duy nhất 1 biểu thức logic (chưa dùng lệnh if).
"""

toan = float(input())  # Nhập điểm Toán
van = float(input())  # Nhập điểm Văn
anh = float(input())  # Nhập điểm Anh
has_certificate = input().strip().lower() == 'true'  # Nhập chứng chỉ (True/False)
# Tính điểm trung bình
average = (toan + van + anh) / 3
# Kiểm tra điều kiện trúng tuyển
ThuocDienTrungTuyen = (toan >= 5.0 and van >= 5.0) and (average >= 6.5 or has_certificate)
print(ThuocDienTrungTuyen)  # In kết quả True/False 
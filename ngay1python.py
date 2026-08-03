"""
Học kiểu dữ liệu nguyên thủy (int float str bool) biến và toán tử
"""



def bai1():
    """
    Bài 1: Tính chỉ số khối cơ thể (BMI)
    Đề bài: Nhập chiều cao và cân nặng, tính BMI và in kết quả.
    """
    can_nang = float(input())
    chieu_cao = float(input())
    bmi = can_nang / (chieu_cao ** 2)
    print(bmi)


def bai2():
    """
    Bài 2: Tính toán tiền điện
    Đề bài: Nhập số phút sử dụng, đổi sang giờ và phút dư.
    """
    minutes = int(input())
    hours = minutes // 60
    remaining_minutes = minutes % 60
    print(f"{hours} giờ và {remaining_minutes} phút")


def bai3():
    """
    Bài 3: Trích xuất và định dạng tên
    Đề bài: Nhập tên, loại bỏ khoảng trắng thừa và in theo chuẩn.
    """
    name = input()
    name = name.strip()
    name = name.title()
    print(name)
    print(name.upper())


def bai4():
    """
    Bài 4: Tạo email tự động từ họ tên
    Đề bài: Nhập họ tên và tạo địa chỉ email theo định dạng company.
    """
    name = input()
    email = name.replace(" ", "").lower() + "@company.com"
    print(email)


def bai5():
    """
    Bài 5: Kiểm tra chuỗi đối xứng
    Đề bài: Nhập chuỗi và kiểm tra xem nó có phải chuỗi đối xứng không.
    """
    string = input()
    string = string.replace(" ", "").lower()
    reversed_string = string[::-1]
    if string == reversed_string:
        print("Đây là chuỗi đối xứng")
    else:
        print("Đây không phải là chuỗi đối xứng")


def bai6():
    """
    Bài 6: Đếm số lần xuất hiện của một ký tự trong chuỗi
    Đề bài: Nhập chuỗi và ký tự, đếm số lần ký tự đó xuất hiện.
    """
    string = input()
    char = input()
    count = string.count(char)
    print(count)


def bai7():
    """
    Bài 7: Lặp chuỗi tạo hình trang trí
    Đề bài: Nhập ký tự và tiêu đề, in khung trang trí bằng ký tự đó.
    """
    char = input()
    title = input()
    border_length = 20
    border = char * border_length
    print(f"{border} {title} {border}")


def bai8():
    """
    Bài 8: Kiểm tra điều kiện xét tuyển
    Đề bài: Nhập điểm và kiểm tra xem thí sinh có đủ điều kiện trúng tuyển không.
    """
    toan = float(input())
    van = float(input())
    anh = float(input())
    has_certificate = input().strip().lower() == 'true'
    average = (toan + van + anh) / 3
    ThuocDienTrungTuyen = (toan >= 5.0 and van >= 5.0) and (average >= 6.5 or has_certificate)
    print(ThuocDienTrungTuyen)


def bai9():
    """
    Bài 9: Đảo ngược số có 3 chữ số
    Đề bài: Nhập số có 3 chữ số, in ra số đảo ngược.
    """
    number = int(input())
    hundreds = number // 100
    tens = (number // 10) % 10
    units = number % 10
    reversed_number = units * 100 + tens * 10 + hundreds
    print(reversed_number)


def bai10():
    """
    Bài 10: Ứng dụng tính hóa đơn bán hàng
    Đề bài: Nhập tên sản phẩm, số lượng, đơn giá và giảm giá, in hóa đơn.
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


if __name__ == "__main__":
    print("Chọn bài muốn chạy:")
    print("1. Bài 1")
    print("2. Bài 2")
    print("3. Bài 3")
    print("4. Bài 4")
    print("5. Bài 5")
    print("6. Bài 6")
    print("7. Bài 7")
    print("8. Bài 8")
    print("9. Bài 9")
    print("10. Bài 10")
    choice = input("Nhập số bài muốn chạy: ").strip()

    exercises = {
        "1": bai1,
        "2": bai2,
        "3": bai3,
        "4": bai4,
        "5": bai5,
        "6": bai6,
        "7": bai7,
        "8": bai8,
        "9": bai9,
        "10": bai10,
    }

    if choice in exercises:
        exercises[choice]()
    else:
        print("Không có bài này")
"""Bài tập Python - Ngày 2

Các bài tập cơ bản: lọc, thống kê, chuẩn hoá dữ liệu.
Tôi đã sửa lỗi indent, tách logic vào hàm, và làm đầu ra rõ ràng hơn.
"""

from typing import List, Any, Dict


def bai1() -> None:
    """Lọc số chẵn và số lẻ từ một danh sách."""
    numbers = [12, 5, 8, 19, 24, 3, 7, 30]
    so_chan = []
    so_le = []
    for n in numbers:
        if n % 2 == 0:
            so_chan.append(n)
        else:
            so_le.append(n)
    print("Bài 1 - Số chẵn:", so_chan)
    print("Bài 1 - Số lẻ:", so_le)


def bai2() -> None:
    """In ra điểm trung bình và các điểm >= trung bình."""
    scores = [6.5, 8.0, 4.5, 9.0, 7.5, 5.0, 8.5]
    average_score = sum(scores) / len(scores)
    print(f"Bài 2 - Điểm trung bình: {average_score:.2f}")
    above_average = []
    for score in scores:
        if score >= average_score:
            above_average.append(score)
    print("Bài 2 - Điểm >= trung bình:", above_average)

def bai3() -> None:
    """Tìm số lớn nhất và nhỏ nhất không dùng max()/min()."""
    data = [15, 22, 8, 19, 31, 5, 12]
    if not data:
        print("Bài 3 - Dữ liệu rỗng")
        return
    max_val = data[0]
    min_val = data[0]
    for n in data:
        if n > max_val:
            max_val = n
        if n < min_val:
            min_val = n
    print("Bài 3 - Lớn nhất:", max_val)
    print("Bài 3 - Nhỏ nhất:", min_val)


def bai4() -> None:
    """Chuẩn hoá tên: loại bỏ khoảng trắng và viết hoa chữ cái đầu."""
    names = ["  Alice", "Bob  ", "  Charlie  ", "David", "Eve"]
    normalized_names = []
    for name in names:
        normalized = name.strip().capitalize()
        normalized_names.append(normalized)
    print("Bài 4 - Tên chuẩn hoá:", normalized_names)


def bai5() -> None:
    """Lấy các phần tử duy nhất theo thứ tự xuất hiện."""
    items = ["apple", "banana", "apple", "orange", "banana", "kiwi"]
    unique_items = []
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    print("Bài 5 - Phần tử duy nhất:", unique_items)


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def bai6() -> None:
    """Lọc và in các số nguyên tố trong danh sách."""
    numbers = [2, 3, 4, 10, 11, 13, 15, 17, 20, 23]
    primes = []
    for n in numbers:
        if is_prime(n):
            primes.append(n)
    print("Bài 6 - Số nguyên tố:", primes)


def bai7() -> None:
    """Tách các phần tử theo kiểu dữ liệu từ danh sách hỗn hợp."""
    mixed_list = [1, "hello", 3.14, True, None, "world", 42]
    integers = []
    strings = []
    booleans = []
    floats = []
    for item in mixed_list:
        # Kiểm tra bool trước int vì bool là subclass của int
        if isinstance(item, bool):
            booleans.append(item)
        elif isinstance(item, int) and not isinstance(item, bool):
            integers.append(item)
        elif isinstance(item, float):
            floats.append(item)
        elif isinstance(item, str):
            strings.append(item)

    print("Bài 7 - Integers:", integers)
    print("Bài 7 - Strings:", strings)
    print("Bài 7 - Booleans:", booleans)
    print("Bài 7 - Floats:", floats)


def bai8() -> None:
    """Lọc sản phẩm có giá < 1.000.000 và in tên của chúng."""
    products = [
        {"name": "Laptop", "price": 15_000_000},
        {"name": "Chuột", "price": 250_000},
        {"name": "Bàn phím", "price": 800_000},
        {"name": "Tai nghe", "price": 450_000},
        {"name": "Màn hình", "price": 3_500_000},
    ]
    cheap = [p["name"] for p in products if p.get("price", 0) < 1_000_000]
    print("Bài 8 - Sản phẩm < 1.000.000:", cheap)


def main() -> None:
    exercises = {
        "1": bai1,
        "2": bai2,
        "3": bai3,
        "4": bai4,
        "5": bai5,
        "6": bai6,
        "7": bai7,
        "8": bai8,
    }

    print("Chương trình Bài tập - Ngày 2")
    while True:
        print("\nChọn bài muốn chạy (1-8) hoặc 'q' để thoát:")
        choice = input().strip()
        if choice.lower() in {"q", "quit", "exit"}:
            print("Thoát chương trình. Hẹn gặp lại!")
            break
        func = exercises.get(choice)
        if func:
            print("--- Bắt đầu ---")
            func()
            print("---- Kết thúc ----")
        else:
            print("Không có bài này, hãy nhập số từ 1 đến 8 hoặc 'q' để thoát.")


if __name__ == "__main__":
    main()
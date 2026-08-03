"""
Cấu trúc dữ liệu List và Tuple (truy cập slice thêm/sửa/xóa)
"""
# Bài 1: Quản lý todo list (append/remove/insert)
# Bài 2: Lấy cắt list (first 3, last 4, vị trí lẻ, đảo ngược)
# Bài 3: Tìm giá trị lớn thứ hai trong list
# Bài 4: Chuyển tuple -> list -> tuple và sửa giá trị
# Bài 5: Chia list thành 3 phần bằng nhau
# Bài 6: Đảo ngược từng chuỗi trong list
# Bài 7: Kết hợp hai list không trùng lặp
# Bài 8: Giải nén tuple đa cấp
# Bài 9: Rút gọn các phần tử lặp liền kề
# Bài 10: Xoay vòng list sang phải

def bai1():
    todos = ["Học Python", "Đọc sách", "Tập thể dục"]
    todos.append("Đi chợ")
    todos.remove("Đọc sách")
    todos.insert(0, "Uống nước")
    print(todos[-1])  # In ra phần tử cuối cùng của danh sách


def bai2():
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # in ra 3 phần tử đầu tiên
    print(numbers[:3])
    # in ra 4 phần tử cuối cùng
    print(numbers[-4:])
    # in ra phần tử ở vị trí lẻ
    print(numbers[1::2])
    # in ra danh sách đảo ngược
    print(numbers[::-1])


def bai3():
    scores = [85, 92, 78, 92, 88, 76, 90]
    unique_scores = []
    for score in scores:
        if score not in unique_scores:
            unique_scores.append(score)
    unique_scores.sort(reverse=True)
    if len(unique_scores) >= 2:
        second_highest = unique_scores[1]
        print(second_highest)
    else:
        print("Không có giá trị thứ hai lớn nhất")


def bai4():
    info = ("Nguyễn Văn A", 2002, "Ha Noi")
    info_list = list(info)
    info_list[1] = 2003
    info_list.append("Việt Nam")
    info = tuple(info_list)
    print(info)


def bai5():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    part_size = len(data) // 3
    for n in range(3):
        part = data[n * part_size: (n + 1) * part_size]
        print(f"Phần {n + 1}: {part}")


def bai6():
    words = ["python", "developer", "data", "pipeline"]
    dao_nguoc_ki_tu = [word[::-1] for word in words]
    print(dao_nguoc_ki_tu)


def bai7():
    list1 = [1, 3, 5, 7, 9]
    list2 = [3, 4, 5, 6, 7]
    ket_qua = list1.copy()
    for item in list2:
        if item not in ket_qua:
            ket_qua.append(item)
    print(ket_qua)


def bai8():
    record = ("P1", (10.5, 20.0), "Active")
    point_name, coordinates, status = record
    x, y = coordinates
    print(f"Point Name: {point_name}, X: {x}, Y: {y}, status: {status}")


def bai9():
    nums = [1, 1, 2, 3, 3, 3, 2, 4, 4, 1]
    unique_nums = []
    for num in nums:
        if not unique_nums or num != unique_nums[-1]:
            unique_nums.append(num)
    print(unique_nums)


def bai10():
    arr = [1, 2, 3, 4, 5, 6, 7]
    k = 3
    arr = arr[-k:] + arr[:-k]
    print(arr)


def main():
    functions = {
        1: bai1,
        2: bai2,
        3: bai3,
        4: bai4,
        5: bai5,
        6: bai6,
        7: bai7,
        8: bai8,
        9: bai9,
        10: bai10,
    }

    while True:
        print("\nChọn bài 1-10 để chạy (0 để thoát):")
        for number in range(1, 11):
            print(f"{number}. Bài {number}")

        try:
            choice = int(input("Bạn chọn: ").strip())
        except ValueError:
            print("Vui lòng nhập số nguyên từ 0 đến 10.")
            continue

        if choice == 0:
            print("Kết thúc chương trình.")
            break
        if choice in functions:
            print(f"--- Kết quả Bài {choice} ---")
            functions[choice]()
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 0 đến 10.")


if __name__ == "__main__":
    main()

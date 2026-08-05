"""
Tổng hợp kiến thức Python từ ngay1python đến ngay5python.
Mỗi phần vừa có mã ví dụ vừa có giải thích lý thuyết.
"""

# Ngày 1: Kiểu dữ liệu, biến, toán tử, input/output và xử lý chuỗi
# - int, float, str, bool
# - đọc dữ liệu từ người dùng với input()
# - ép kiểu bằng int(), float(), str()
# - toán tử số học và toán tử chuỗi
# - thao tác chuỗi: strip(), lower(), upper(), replace(), title()


def ngay1_bmi(can_nang, chieu_cao):
    """Tính chỉ số BMI.

    BMI dùng để ước lượng lượng mỡ cơ thể theo cân nặng và chiều cao.
    - can_nang: cân nặng tính bằng kg
    - chieu_cao: chiều cao tính bằng mét

    Giá trị trả về: một số thực. Khi BMI lớn, nghĩa là cân nặng so với chiều cao lớn.
    Dùng hàm này để kiểm tra cơ bản xem cân nặng nằm trong mức bình thường hay không.
    """
    return can_nang / (chieu_cao ** 2)


def ngay1_format_name(name):
    """Chuẩn hóa tên người dùng.

    - strip() loại bỏ khoảng trắng thừa ở đầu và cuối.
    - title() viết hoa chữ cái đầu mỗi từ.

    Hàm này hữu ích khi muốn lưu tên đẹp và nhất quán.
    """
    return name.strip().title()


def ngay1_is_palindrome(text):
    """Kiểm tra chuỗi đối xứng.

    Một chuỗi đối xứng là chuỗi đọc xuôi và đọc ngược giống nhau.
    Loại bỏ dấu cách và chuyển về chữ thường để so sánh chính xác.
    """
    normalized = text.replace(" ", "").lower()
    return normalized == normalized[::-1]


# Ngày 2: Cấu trúc điều kiện và vòng lặp
# - if / else / elif
# - for / while
# - toán tử so sánh và logic
# - dùng list để lưu kết quả và lọc dữ liệu


def ngay2_split_even_odd(numbers):
    """Tách danh sách thành số chẵn và số lẻ.

    - if kiểm tra điều kiện chia hết cho 2.
    - append() thêm phần tử vào list.
    """
    even = []
    odd = []
    for n in numbers:
        if n % 2 == 0:
            even.append(n)
        else:
            odd.append(n)
    return even, odd


def ngay2_average(scores):
    """Tính điểm trung bình.

    - sum() lấy tổng.
    - len() lấy số lượng phần tử.
    - nếu danh sách rỗng thì tránh chia cho 0.
    """
    return sum(scores) / len(scores) if scores else 0


def ngay2_find_min_max(values):
    """Tìm min và max mà không dùng hàm có sẵn.

    - duyệt từng giá trị với for.
    - so sánh để cập nhật giá trị nhỏ nhất và lớn nhất.
    """
    if not values:
        return None, None
    min_val = max_val = values[0]
    for v in values:
        if v < min_val:
            min_val = v
        if v > max_val:
            max_val = v
    return min_val, max_val


def ngay2_is_prime(n):
    """Kiểm tra số nguyên tố.

    - Số nguyên tố chỉ chia hết cho 1 và chính nó.
    - Nếu chia hết cho 2 thì không phải số nguyên tố (ngoại trừ 2).
    - Chỉ kiểm tra ước lẻ đến căn bậc hai của số.
    """
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


# Ngày 3: List và Tuple
# - tạo list, truy cập phần tử và slicing
# - thêm / xóa / sửa phần tử với append/remove/insert
# - chuyển đổi tuple -> list -> tuple
# - cắt danh sách, đảo danh sách, loại bỏ phần tử trùng liền kề


def ngay3_unique_ordered(items):
    """Giữ lại các phần tử duy nhất theo thứ tự xuất hiện.

    - Duyệt list từng phần tử.
    - Nếu phần tử chưa xuất hiện trong result thì thêm.
    """
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def ngay3_rotate_right(arr, k):
    """Xoay list sang phải k vị trí.

    - k % len(arr): đảm bảo k không lớn hơn độ dài list.
    - slicing arr[-k:] lấy k phần tử cuối.
    """
    k = k % len(arr)
    return arr[-k:] + arr[:-k]


# Ngày 4: Dictionary và Set
# - lưu trữ dữ liệu theo cặp key-value
# - duyệt danh sách dictionary
# - tính tổng theo nhóm
# - chuẩn hóa dữ liệu và lọc theo điều kiện


def ngay4_group_sum(records, key_field, value_field):
    """Tính tổng theo một nhóm nào đó trong danh sách.

    - records là một danh sách dictionary.
    - mỗi dictionary có key_field và value_field.
    - totals[key] lưu tổng giá trị cho mỗi nhóm.
    """
    totals = {}
    for record in records:
        key = record[key_field]
        value = record[value_field]
        totals[key] = totals.get(key, 0) + value
    return totals


def ngay4_filter_products(products, max_price):
    """Lọc sản phẩm theo giá và trạng thái còn hàng.

    - list comprehension giúp tạo list mới nhanh gọn.
    - p.get('price', 0) đảm bảo không lỗi nếu thiếu trường price.
    """
    return [p["name"] for p in products if p.get("price", 0) < max_price and p.get("in_stock")]


# Ngày 5: Hàm, đối số linh hoạt, đệ quy và xử lý dữ liệu nâng cao
# - định nghĩa hàm và trả về giá trị
# - *args, **kwargs
# - đệ quy đơn giản
# - xử lý chuỗi, list và dictionary


def ngay5_average(*args):
    """Tính trung bình từ nhiều giá trị.

    *args cho phép truyền nhiều số vào một hàm.
    """
    if not args:
        return 0
    return sum(args) / len(args)


def ngay5_profile(first_name, last_name, **info):
    """Tạo dictionary profile linh hoạt.

    **info cho phép thêm nhiều thông tin như age, city, email.
    """
    profile = {"first_name": first_name, "last_name": last_name}
    profile.update(info)
    return profile


def ngay5_reverse_string(s):
    """Đảo chữ của một chuỗi bằng đệ quy.

    Đệ quy chia bài toán thành phần nhỏ hơn: lấy ký tự cuối cùng, sau đó gọi lại chính hàm với phần còn lại.
    """
    if len(s) <= 1:
        return s
    return s[-1] + ngay5_reverse_string(s[:-1])


def ngay5_word_frequency(text):
    """Đếm tần suất từ trong một chuỗi văn bản.

    - text.lower() để không phân biệt hoa thường.
    - split() để tách các từ.
    - dùng dict để lưu số lần xuất hiện.
    """
    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def ngay5_checkout(cart, products):
    """Tính tổng tiền thanh toán của giỏ hàng.

    - cart là danh sách cặp (product_id, quantity)
    - products lưu thông tin giá và stock theo product_id
    - bỏ qua sản phẩm không tồn tại hoặc số lượng không hợp lệ
    """
    total = 0
    for product_id, quantity in cart:
        if product_id not in products:
            continue
        product = products[product_id]
        if quantity <= 0 or product["stock"] < quantity:
            continue
        total += product["price"] * quantity
    return total


if __name__ == "__main__":
    print("Tổng hợp kiến thức Python từ ngày 1 đến ngày 5")
    print("Ngày 1: BMI, xử lý chuỗi, định dạng, đối xứng")
    print("Ngày 2: điều kiện, vòng lặp, tìm min/max, số nguyên tố")
    print("Ngày 3: list/tuple, slicing, duyệt, xoay vòng")
    print("Ngày 4: dictionary, tổng nhóm, lọc sản phẩm")
    print("Ngày 5: hàm, *args/**kwargs, đệ quy, tần suất từ, thanh toán giỏ hàng")

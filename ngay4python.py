"""
Cấu trúc dữ liệu Dictionary và Set (Key-Value HashSet)
"""

# File này chứa các bài tập Python xử lý Dictionary, Set và dữ liệu dạng key-value.
# Chạy menu bên dưới để chọn bài 1-8 và xem kết quả tương ứng.

def bai1():
    employees = [
        {"id": "NV01", "name": "Nguyễn Văn An", "department": "IT", "salary": 18000000},
        {"id": "NV02", "name": "Trần Thị Bích", "department": "HR", "salary": 12000000},
        {"id": "NV03", "name": "Lê Hoàng Cường", "department": "IT", "salary": 25000000}
    ]
    for employee in employees:
        dinh_dang_luong = "{:,}".format(employee["salary"]).replace(",", ".")
        empoyee_id = employee["id"]
        print(f"ID: {employee['id']}, Name: {employee['name']}, Department: {employee['department']}, salary: {dinh_dang_luong} VND")

def bai2():
    products = [
        {"name": "Laptop Dell", "price": 15000000, "in_stock": True},
        {"name": "Chuột Logitech", "price": 350000, "in_stock": False},
        {"name": "Bàn phím Akko", "price": 1200000, "in_stock": True},
        {"name": "Màn hình LG", "price": 4500000, "in_stock": False}
    ]
    for product in products:
        dinh_dang_gia = "{:,}".format(product["price"]).replace(",", ".")
        if product["price"] < 5000000 and product["in_stock"] == True:
            print(f"Product Name: {product['name']}, Price: {dinh_dang_gia}, In Stock: {product['in_stock']}")

def bai3():
    students = [
        {"name": "An", "math": 8.5, "physics": 7.0},
        {"name": "Bình", "math": 9.0, "physics": 9.5},
        {"name": "Cường", "math": 6.0, "physics": 8.0}
    ]
    avg_score_math = sum(student["math"] for student in students) / len(students)
    avg_score_physics = sum(student["physics"] for student in students) / len(students)
    print(avg_score_math, avg_score_physics)

def bai4():
    posts = [
        {"id": 101, "title": "Học Python cơ bản", "views": 1500, "likes": 230},
        {"id": 102, "title": "Data Engineering là gì?", "views": 4200, "likes": 580},
        {"id": 103, "title": "Mẹo dùng List Comprehension", "views": 3100, "likes": 410}
    ]
    max_post = posts[0]
    min_post = posts[0]
    for post in posts:
        if post["likes"] > max_post["likes"]:
            max_post = post
        if post["likes"] < min_post["likes"]:
            min_post = post
    print(max_post, min_post)

def bai5():
    orders = [
        {"order_id": 1, "category": "Điện thoại", "amount": 10000000},
        {"order_id": 2, "category": "Phụ kiện", "amount": 200000},
        {"order_id": 3, "category": "Điện thoại", "amount": 15000000},
        {"order_id": 4, "category": "Phụ kiện", "amount": 500000},
        {"order_id": 5, "category": "Gia dụng", "amount": 2000000}
    ]
    revenue_category = {}
    for order in orders:
        cat = order['category']
        amt = order['amount']
        if cat in revenue_category:
            revenue_category[cat] += amt
        else:
            revenue_category[cat] = amt
    print(revenue_category)

def bai6():
    cart = [
        {"item": "Áo sơ mi", "price": 300000, "quantity": 2, "tags": ["thời trang", "nam"]},
        {"item": "Quần Jean", "price": 500000, "quantity": 1, "tags": ["thời trang", "nam", "giảm giá"]},
        {"item": "Bình nước", "price": 100000, "quantity": 3, "tags": ["gia dụng"]}
    ]
    total_amount = 0
    for item in cart:
        total_amount += item['price'] * item['quantity']
    discounted_item = []
    for item in cart:
        if "giảm giá" in item['tags']:
            discounted_item.append(item['item'])
    print(total_amount)
    print(discounted_item)

def bai7():
    users = [
        {"username": "  an_nguyen ", "role": "admin", "active": True},
        {"username": "binh_tran", "role": "user", "active": False},
        {"username": "cuong_le  ", "role": "user", "active": True}
    ]
    for user in users:
        user['username'] = user["username"].strip().upper()
        if user['role'] == "user":
            user['active'] = False
        print(user)

def bai8():
    users = [
        {"user_id": 1, "name": "An"},
        {"user_id": 2, "name": "Bình"},
        {"user_id": 3, "name": "Cường"}
    ]

    orders = [
        {"order_id": 101, "user_id": 1, "total": 500000},
        {"order_id": 102, "user_id": 2, "total": 300000},
        {"order_id": 103, "user_id": 1, "total": 150000}
    ]
    user_map = {user['user_id']: user['name'] for user in users}
    order_details = []
    for order in orders:
        if order['user_id'] in user_map:
            order_details.append({
                "order_id": order['order_id'],
                "user_name": user_map[order['user_id']],
                "total": order['total']
            })
    import pprint
    pprint.pprint(order_details)


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
    }

    while True:
        print("\nChọn bài 1-8 để chạy (0 để thoát):")
        for number in range(1, 9):
            print(f"{number}. Bài {number}")

        try:
            choice = int(input("Bạn chọn: ").strip())
        except ValueError:
            print("Vui lòng nhập số nguyên từ 0 đến 8.")
            continue

        if choice == 0:
            print("Kết thúc chương trình.")
            break
        if choice in functions:
            print(f"--- Kết quả Bài {choice} ---")
            functions[choice]()
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 0 đến 8.")


if __name__ == "__main__":
    main()

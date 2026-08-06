#bai1
def calculate_average(*args):
    if not args:
        return 0
    return sum(args) / len(args)
print(calculate_average([1, 2, 3, 4, 5]))
#bai2
def build_profile(first_name, last_name, **kwargs):
    profile = {
        'first_name': first_name,
        'last_name': last_name,
    }
    profile.update(kwargs)
    return profile
print(build_profile('John', 'Doe', age=30, location='New York'))
#bai3
def filter_even_odd(numbers, mode="even"):
    if mode == "even":
        return [x for x in numbers if x % 2 == 0]
    elif mode == "odd":
        return [x for x in numbers if x % 2 != 0]
    else:
        return []
print(filter_even_odd([1, 2, 3, 4, 5], mode="even"))
#bai4
def reverse_string(s):
    if len(s) <=1:
        return s
    else:
        return s[-1] + reverse_string(s[:-1])
print(reverse_string("hello"))
#bai5
def process_scores(min_pass, *scores, **metadata):
    qua = [diem for diem in scores if diem >=min_pass]
    tach = [diem for diem in scores if diem < min_pass]
    result = {
        'qua' : qua,
        'tach': tach
    }
    result.update(metadata)
    return result
print(process_scores(5.0, 3.5, 6.0, 8.0, 4.0, subject="DSA", semester=1))
#bai1 phan 2
def format_user_data(full_name, phone_number):
    words = full_name.strip().split()
    clean_name = " ".join([w.capitalize() for w in words])
    clean_phone = phone_number.strip()
    if clean_phone.startswith('0'):
        clean_phone = "+84" + clean_phone[1:]
    return clean_name,clean_phone
print(format_user_data(" dk sklic sfjfju","02929139"))
#bai2 phan 2
def analyze_numbers(numbers):
    max_val = numbers[0];
    even = [number for number in numbers if number %2==0]
    odd = [number for number in numbers if number %2!=0]
    avg_even = sum(even) / len(even)
    odd_count = len(odd)
    for number in numbers:
        if number > max_val:
            max_val = number
    dic = {
        'avg_even' : avg_even,
        'odd_count' :odd_count ,
        'max' : max_val
    }
    print(dic)
analyze_numbers([1,2,3,4,5,6])
#bai3 phan 2
def word_frequency(text):
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

print(word_frequency("The quick brown fox jumps over the lazy dog"))
#bai4 phan 2
list_a = []
list_b = []
def find_unique_common(list_a, list_b):
    set_a = set(list_a)
    set_b = set(list_b)
    unique_common = set_a.intersection(set_b)
    return list(unique_common)
print(find_unique_common([1, 2, 3, 4], [3, 4, 5, 6]))
#bai5 phan 2
students = [
    {"name": "An", "scores": [8, 9, 7]},
    {"name": "Binh", "scores": [4, 5, 6]},
    {"name": "Cuong", "scores": [9, 9, 10]}
]
def process_students(students):
    avg_scores = []
    for student in students:
        avg_score = sum(student["scores"]) / len(student["scores"])
        if avg_score >= 7:
         avg_scores.append({"name": student["name"], "gpa": round(avg_score, 2)})
    return avg_scores
print(process_students(students))
#bai6 phan 2
def recursive_reverse(s):
    if len(s) <=1:
        return s
    else:
        return s[-1]+ recursive_reverse(s[:-1])
print(recursive_reverse("hello"))
#bai7 phan 2

#bai8 phan 2
def create_config(app_name, **kwargs):
    cau_hinh = {
        "app_name": app_name, 
        "version": "1.0", 
        "debug": False, 
        "theme": "light"
    }
    cau_hinh.update(kwargs)
    return cau_hinh
print(create_config('shopee',size = "100mb"))
#bai8 phan 2
def smart_sum(*args):
    total = 0
    for a in args:
     if(isinstance(a,int) or isinstance(a,float)) and type(a) is not bool:
      total += a
    return total
print(smart_sum(1, 2.5, "hello", True, 3))
#bai 9 phan 2
def most_frequent(arr):
    if not arr:
        return None

    count_max = {}
    for item in arr:
        count_max[item] = count_max.get(item, 0) + 1

    most_common = None
    max_count = 0
    for item, count in count_max.items():
        if count > max_count:
            max_count = count
            most_common = item

    return most_common

print(most_frequent([1, 2, 3, 2, 3, 3, 3, 1, 6]))
#bai10 phan 2
products = {
    "P1": {"name": "Laptop", "price": 1000, "stock": 5},
    "P2": {"name": "Phone", "price": 500, "stock": 10},
    "P3": {"name": "Mouse", "price": 20, "stock": 0}
}

# Hàm thanh toán giỏ hàng.
# cart là danh sách các cặp (product_id, quantity).
def checkout(cart, products):
    total_bill = 0

    for product_id, quantity in cart:
        if product_id not in products:
            print(f"Sản phẩm {product_id} không tồn tại.")
            continue

        product = products[product_id]
        if quantity <= 0:
            print(f"Số lượng cho {product_id} phải lớn hơn 0.")
            continue

        if product["stock"] < quantity:
            print(f"{product['name']} chỉ còn {product['stock']} chiếc. Không thể mua {quantity}.")
            continue

        price = product["price"]
        item_total = price * quantity
        total_bill += item_total

        print(f"{product['name']}: {quantity} x {price} = {item_total}")

    return total_bill


def main():
    cart = [("P1", 1), ("P2", 2), ("P3", 1), ("P4", 1)]
    print("Giỏ hàng:", cart)
    total = checkout(cart, products)
    print("Tổng tiền phải trả:", total)


if __name__ == "__main__":
    main()

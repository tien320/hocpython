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
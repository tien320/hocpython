products = [
    {"name": "Laptop", "price": 15000000},
    {"name": "Chuột", "price": 250000},
    {"name": "Bàn phím", "price": 800000},
    {"name": "Tai nghe", "price": 450000},
    {"name": "Màn hình", "price": 3500000}
]
danh_sach_san_pham = []  # Danh sách chứa các sản phẩm có giá < 1 triệu
for product in products:
    if product["price"] < 1000000:
        danh_sach_san_pham.append(product["name"])  # Thêm sản phẩm vào danh sách mới
print(danh_sach_san_pham)  # In danh sách các sản phẩm có giá < 1 triệu
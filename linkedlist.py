class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Thêm vào cuối danh sách: O(N)
    def append(self, val):
        new_node = Node(val)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    # Chèn giá trị x vào vị trí chỉ số k (0-indexed)
    def insert_at(self, val, k):
        new_node = Node(val)
        # Chèn vào đầu
        if k == 0:
            new_node.next = self.head
            self.head = new_node
            return

        curr = self.head
        # Duyệt tới nút đứng ngay trước vị trí cần chèn (vị trí k-1)
        for _ in range(k - 1):
            if curr is None:
                break
            curr = curr.next

        if curr is None:
            print(f"Vị trí {k} vượt quá độ dài danh sách!")
            return

        # Nối con trỏ: Nút mới trỏ tới nút sau, nút trước trỏ tới nút mới
        new_node.next = curr.next
        curr.next = new_node

    # Xóa nút đầu tiên có giá trị bằng target
    def delete_value(self, target):
        if not self.head:
            return

        # Nếu nút cần xóa là Head
        if self.head.val == target:
            self.head = self.head.next
            return

        curr = self.head
        while curr.next and curr.next.val != target:
            curr = curr.next

        # Bỏ qua nút cần xóa bằng cách nối thẳng sang nút kế tiếp
        if curr.next:
            curr.next = curr.next.next

    # Đảo ngược toàn bộ danh sách liên kết: O(N) thời gian, O(1) bộ nhớ
    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            next_temp = curr.next  # 1. Lưu lại nút phía sau để không bị mất dấu
            curr.next = prev       # 2. Đảo chiều mũi tên quay ngược về trước
            prev = curr            # 3. Tiến con trỏ prev lên
            curr = next_temp       # 4. Tiến con trỏ curr lên
        self.head = prev

    # Hàm in danh sách
    def display(self):
        nodes = []
        curr = self.head
        while curr:
            nodes.append(str(curr.val))
            curr = curr.next
        nodes.append("None")
        print(" -> ".join(nodes))


# ==================== CHẠY THỰC TẾ TỪNG BƯỚC ====================

ll = LinkedList()

# Bước 1: Khởi tạo danh sách ban đầu [5, 7, 4, 1]
for x in [5, 7, 4, 1]:
    ll.append(x)
print("1. Danh sách ban đầu:")
ll.display()

# Bước 2: Chèn giá trị 99 vào vị trí chỉ số k = 2 (chèn giữa 7 và 4)
print("\n2. Chèn số 99 vào vị trí k = 2:")
ll.insert_at(val=99, k=2)
ll.display()

# Bước 3: Xóa phần tử có giá trị 7
print("\n3. Xóa phần tử có giá trị 7:")
ll.delete_value(target=7)
ll.display()

# Bước 4: Đảo ngược danh sách liên kết
print("\n4. Đảo ngược toàn bộ danh sách:")
ll.reverse()
ll.display()
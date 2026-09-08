from repository import UserRepository
from user import User
class UserApp:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    def input_user(self):
        while True:
            user_id = input("nhập id: ").strip()
            user_name = input("nhập tên: ").strip()
            email = input("nhập email: ").strip()
            role = input("nhập role: ").strip()
            user = User(user_id, user_name, email, role)
            self.repo.add(user)
            choice = input("bạn có muốn nhập tiếp không (y/n): ").strip().lower()
            if choice != "y":
                break
    def show_all(self):
        user = self.repo.list_all()
        if not user:
            print("ko có")
            return
        for u in user:
            print(u)
    def update_user(self):
        user_id = input("nhập id cần upadate: ").strip()
        user = self.repo.find_by_id(user_id)
        if not user:
            print("ko có")
            return
        print("sửa thông tin")
        new_name = input("tên mới: ")
        new_email = input("emai mới: ")
        new_role = input("role mới: ")
        result = self.repo.update(user_id,new_name,new_email,new_role)
        if result:
            print("cập nhật thành công")
        else:
            print("lỗi")
    def delete_user(self):
        user_id = input("nhập id cần xóa: ").strip()
        user = self.repo.find_by_id(user_id)
        if not user:
            print("ko có")
            return
        result = self.repo.delete(user_id)
        if result:
            print("đã xóa")
        else:
            print("lỗi")
    def search_by_role(self):
        role = input("nhập vai trò cần tìm: ")
        result = self.repo.find_by_role(role)
        if not result:
            print("ko tìm thấy")
            return
        for user in result:
            print(user)
    def search_by_email(self):
        email = input("nhập email cần tìm: ")
        result = self.repo.find_by_email(email)
        if not result:
            print("ko tìm thấy")
            return
        for user in result:
            print(user)
    def run_menu(self):
        while True:
            print("chọn chương trình")
            print("0.thoát")
            print("1.xem tất cả")
            print("2.tìm theo role")
            print("3.tìm theo email")
            print("4.update thông tin")
            print("5.xóa user")
            print("6.thêm user")
            choice = input("chọn chương trình: ").strip()
            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.search_by_role()
            elif choice == "3":
                self.search_by_email()
            elif choice == "4":
                self.update_user()
            elif choice == "5":
                self.delete_user()
            elif choice == "6":
                self.input_user()
            elif choice == "0":
                print("đã thoát")
                break
            else:
                print("lỗi nhập số")

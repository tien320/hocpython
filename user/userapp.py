from databaserepository import DatabaseRepository
from user import User

class UserApp:
    def __init__(self, repo : DatabaseRepository):
        self.repo = repo
    def input_user(self):
        while True:
            try:
                user_id = int(input("nhập id user: "))
                name = input("nhập tên user: ").strip()
                email = input("nhập email: ").strip()
                role = input("nhập vai trò (admin/user): ").strip()
                new_user = User(user_id,name,email,role)
                if self.repo.add_user(new_user):
                    print("đã thêm thành công")
                else:
                    print("lỗi thêm dữ liệu")
            except ValueError:
                print("ID phải là số nguyên")
            cont = input("nhập tiếp ko (y/n)?: ")
            if cont.strip().lower() != "y":
                break
    def show_all(self):
        user = self.repo.list_all()
        if not user:
            print("ko có")
            return
        for u in user:
            print(u)
    def search_by_email(self):
        email = input("Nhập email cần tìm: ").strip()
        user = self.repo.find_by_email(email)
        if not user:
            print("Không tìm thấy người dùng!")
            return
        print(user)
    def update(self):
        try:
            user_id = int(input("nhập id user: "))
        except ValueError:
            print("ID phải là số nguyên")
            return
        user = self.repo.find_by_id(user_id)
        if not user:
            print("ko có")
            return
        new_name = input("nhập tên mới: ").strip()
        new_email = input("nhập email mới: ").strip()
        new_role = input("nhập chức vụ mới: ").strip()
        result = self.repo.update(user_id,new_name,new_email,new_role)
        if result:
            print("đã update thành công")
        else:
            print("update thất bại")
    def delete(self):
        try:
            user_id = int(input("nhập id user: "))
        except ValueError:
            print("ID phải là số nguyên")
            return
        user = self.repo.find_by_id(user_id)
        if not user:
            print("ko có")
            return
        result = self.repo.delete(user_id)
        if result:
            print("đã xóa thành công")
        else:
            print("xóa thất bại")
    def run_menu(self):
        while True:
                print("Quản lí sinh user")
                print("0.thoát")
                print("1.hiển thị tất cả")
                print("2.update dữ liệu")
                print("3.xóa dữ liệu")
                print("4.thêm dữ liệu")
                print("5.tìm theo email")
                choice = input("chọn yêu cầu: ")
                if choice == "1":
                    self.show_all()
                elif choice == "2":
                    self.update()
                elif choice == "3":
                    self.delete()
                elif choice == "4":
                    self.input_user()
                elif choice == "5":
                    self.search_by_email()
                elif choice == "0":
                    print("đã thoát")
                    break
                else:
                    print("lỗi nhập số")



        
from repository import StudentRepository
from sinhvien import Student

class StudentApp:
    def __init__(self, repo : StudentRepository):
        self.repo = repo
    def input_student(self):
        while True:
            student_id = int(input("nhập id: "))
            while self.repo.exist_id(student_id) :
                print("đã tồn tại id")
                student_id = int(input("nhập lại: "))
            name = input("nhập tên: ")
            age = int(input("nhập tuổi: "))
            gpa = float(input("nhập gpa: "))
            student = Student(student_id, name, age, gpa)
            self.repo.add(student)
            cont = input("tiếp tục nhập (y/n)? ")
            if cont.lower() != 'y':
                break
    def show_all(self):
        sinhvien = self.repo.list_all()
        if not sinhvien:
            print("ko có")
            return
        for s in sinhvien:
            print(s)
    def search_by_name(self):
        ten = input("nhập tên cần tìm: ")
        result  = self.repo.find_by_name(ten)
        if not result :
            print("ko tìm thấy")
            return
        for student in result:
            print(student)
    def update(self):
        student_id = int(input("nhập id cần update: "))
        student = self.repo.find_by_id(student_id)
        if not student:
            print("ko có")
            return
        new_name = input("nhập tên mới: ").strip()
        new_age = int(input("nhập tuổi mới: "))
        new_gpa = float(input("nhập gpa mới: "))
        result = self.repo.update(student_id,new_name,new_age,new_gpa)
        if result:
            print("update thành công")
        else:
            print("lỗi")
    def delete(self):
        student_id = int(input("nhập id cần xóa: "))
        result = self.repo.delete(student_id)
        if result:
            print("đã xóa")
        else:
            print("lỗi")
    def run_menu(self):
        while True:
            print("1. Xem tất cả")
            print("2. Tìm theo tên")
            print("3. Cập nhật")
            print("4. Xóa")
            print("5. Thêm mới")
            print("0. Thoát")
        
            choice = input("Chọn chức năng: ").strip()
            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.search_by_name()
            elif choice == "3":
                self.update()
            elif choice == "4":
                self.delete()
            elif choice == "5":
                self.input_student()
            elif choice == "0":
                print("Đã thoát chương trình.")
                break
            else:
                print("Lựa chọn không hợp lệ!")    
    
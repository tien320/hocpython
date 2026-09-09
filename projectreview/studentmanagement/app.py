from repository import StudentRepository
from student import Student

class StudentApp:
    def __init__(self, repo: StudentRepository):
        self.repo = repo
    def input_student(self):
        while True:
            student_id = int(input("nhập id: "))
            name = input("nhập tên: ").strip()
            age = int(input("nhập tuổi: "))
            email = input("nhập email: ").strip()
            gpa = float(input("nhập gpa: "))
            self.repo.add(Student(student_id,name,age,email,gpa))
            cont = input("nhập tiếp ko? (y/n)")
            if cont.lower() != "y":
                break
    def show_all(self):
        student = self.repo.list_all()
        if not student:
            print("ko có")
            return
        for s in student:
            print(s)
    def update(self):
        student_id = int(input("nhập id cần update: "))
        student = self.repo.find_by_id(student_id)
        if not student:
            print("ko có")
            return
        new_name = input("nhập tên mới: ").strip()
        new_age = int(input("nhập tuổi mới: "))
        new_email = input("nhập email mới: ").strip()
        new_gpa = float(input("nhập gpa mới: "))
        result = self.repo.update(student_id,new_name,new_age,new_email,new_gpa)
        if result:
            print("update thành công")
        else:
            print("lỗi")
    def delete(self):
        student_id = int(input("nhập id cần xóa: "))
        student = self.repo.find_by_id(student_id)
        if not student:
            print("ko có")
            return
        result = self.repo.delete(student_id)
        if result :
            print("xóa thành công")
        else:
            print("lỗi")
    def run_menu(self):
        while True:
            print("Quản lí sinh viên")
            print("0.thoát")
            print("1.hiển thị tất cả")
            print("2.update dữ liệu")
            print("3.xóa dữ liệu")
            print("4.thêm dữ liệu")
            choice = input("chọn yêu cầu: ")
            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.update()
            elif choice == "3":
                self.delete()
            elif choice == "4":
                self.input_student()
            elif choice == "0":
                print("đã thoát")
                break
            else:
                print("lỗi nhập số")
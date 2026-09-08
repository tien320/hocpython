from repository import StudentRepository
from sinhvien import Student

class StudentApp:
    def __init__(self, repo : StudentRepository):
        self.repo = repo
    def input_student(self):
        so_luong = int(input("nhập số lượng: "))
        for i in range(so_luong):
            s_id = input("mã sv: ").strip()
            name = input("tên: ").strip()
            age = int(input("tuổi: "))
            gpa = float(input("GPA: "))
            self.repo.add(Student(s_id,name,age,gpa))
    def search(self):
        ten = input("nhập tên cần tìm: ")
        result  = self.repo.find_by_name(ten)
        if not result :
            print("ko tìm thấy")
            return
        for student in result:
            print(student)
        
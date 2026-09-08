from repository import StudentRepository
from student import Student

class StudentApp:
    def __init__(self, repo: StudentRepository):
        self.repo = repo

    def input_students(self) -> None:
        try:
            count = int(input("Nhập số lượng sinh viên: "))
        except ValueError:
            print("Lỗi: Vui lòng nhập số nguyên!")
            return

        for i in range(count):
            print(f"\n--- Sinh viên #{i + 1} ---")
            s_id = input("Mã SV: ").strip()
            name = input("Họ tên: ").strip()
            age = int(input("Tuổi: "))
            gpa = float(input("GPA: "))

            self.repo.add(Student(s_id, name, age, gpa))

    def search_student(self) -> None:
        keyword = input("\nNhập tên sinh viên cần tìm: ")
        results = self.repo.find_by_name(keyword)

        if not results:
            print(f"Không tìm thấy sinh viên nào chứa tên '{keyword}'.")
            return

        print(f"\nTìm thấy {len(results)} kết quả:")
        for student in results:
            print(student)
from student import Student

class StudentRepository:
    def __init__(self):
        self.storage = []
    def add(self, student: Student):
        self.storage.append(student)
    def list_all(self):
        return list(self.storage)
    def find_by_id(self, student_id: int):
        for u in self.storage:
            if u.id == student_id:
                return u
        return None
    def update(self, student_id: int, new_name: str, new_age: int, new_email: str, new_gpa: float):
        student = self.find_by_id(student_id)
        if new_name.strip():
            student.name = new_name.strip()
        if new_age is not None:
            student.age = new_age
        if new_email.strip():
            student.email = new_email
        if new_gpa is not None:
            student.gpa = new_gpa
        return True
    def delete(self,student_id: int):
        student = self.find_by_id(student_id)
        if not student:
            return False
        self.storage.remove(student)
        return True


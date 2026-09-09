from sinhvien import Student

class StudentRepository:
    def __init__(self):
        self.storage = []
    def add(self, student : Student):
        self.storage.append(student)
    def exist_id(self,student_id:int):
        return self.find_by_id(student_id) is not None
    def list_all(self):
        return list(self.storage)
    def find_by_id(self, student_id: int):
        for u in self.storage:
            if u.student_id == student_id:
                return u
        return None
    def find_by_name(self, ten: str):
        ten = ten.strip().lower()
        result = []
        for s in self.storage:
            if ten in s.name.lower():
                result.append(s)
        return result
    def update(self, student_id: int, new_name: str, new_age: int, new_gpa: float):
        student = self.find_by_id(student_id)
        if not student:
            return False
        if new_name.strip():
            student.name = new_name.strip()
        if new_age is not None:
            student.age = new_age
        if new_gpa is not None:
            student.gpa = new_gpa
        return True
    def delete(self, student_id: int):
        student = self.find_by_id(student_id)
        if not student:
            return False
        self.storage.remove(student)
        return True      
        


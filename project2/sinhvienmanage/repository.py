from sinhvien import Student

class StudentRepository:
    def __init__(self):
        self.storage = []
    def add(self, student : Student):
        self.storage.append(student)
    def find_by_name(self, ten: str):
        ten = ten.strip().lower()
        result = []
        for s in self.storage:
            if ten in s.name.lower():
                result.append(s)
        return result
        
        


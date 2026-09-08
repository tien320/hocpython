class Student:
    def __init__ (self, student_id: int ,name: str, age: int, gpa: float):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gpa = gpa
    def __str__(self):
        return f"id: {self.student_id}, Tên: {self.name}, Tuổi: {self.age}, GPA: {self.gpa}"
    
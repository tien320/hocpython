class Student:
    def __init__(self, student_id: str, name: str, age: int, gpa: float):
        self.id = student_id
        self.name = name
        self.age = age
        self.gpa = gpa

    def __str__(self) -> str:
        return f"[ID: {self.id}] Tên: {self.name} | Tuổi: {self.age} | GPA: {self.gpa:.2f}"
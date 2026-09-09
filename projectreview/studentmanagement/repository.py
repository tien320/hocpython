from student import Student
import sqlite3
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
class DatabaseRepository:
    def __init__(self, db_name: str = "student.db"):
        self.db_name = db_name
        self._create_table()
    def getconnection(self):
        return sqlite3.connect(self.db_name)
    def _create_table(self):
        with self.getconnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                create table student(
                    student_id integer primary key
                    age integer
                    name text not null
                    gpa real not null
                )
            """)
        conn.commit()

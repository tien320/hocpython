from typing import List
from student import Student

class StudentRepository:
    def __init__(self):
        self._storage: List[Student] = []

    def add(self, student: Student) -> None:
        self._storage.append(student)

    def find_by_name(self, keyword: str) -> List[Student]:
        # SELECT * FROM students WHERE LOWER(name) LIKE '%keyword%'
        keyword_clean = keyword.strip().lower()
        return [
            s for s in self._storage 
            if keyword_clean in s.name.lower()
        ]
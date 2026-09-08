from repository import StudentRepository
from app import StudentApp

def main():
    repo = StudentRepository()
    app = StudentApp(repo)
    app.input_students()
    app.search_student()

if __name__ == "__main__":
    main()
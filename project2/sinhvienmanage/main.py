from repository import StudentRepository
from app import StudentApp

def main():
    repo = StudentRepository()
    app = StudentApp(repo)
    app.input_student()
    app.run_menu()
if __name__ == "__main__":
    main()
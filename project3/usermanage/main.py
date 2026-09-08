from repository import UserRepository
from app import UserApp

def main():
    repo = UserRepository("users.json")
    app = UserApp(repo)
    app.input_user()
    app.run_menu()
if __name__ == "__main__":
    main()
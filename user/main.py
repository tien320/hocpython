from userapp import UserApp
from databaserepository import DatabaseRepository

def main():
    repo = DatabaseRepository()
    app = UserApp(repo)
    app.run_menu()
if __name__ == "__main__":
    main()
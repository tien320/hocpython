from fastapi import FastAPI
from models.user import User
from repositories.userepository import UserRepository
from core.database import Database
app = FastAPI()
user_repo = UserRepository(Database())

@app.get("/")
def read_root():
    return {"message": "đang hoạt động"}
@app.post("/user")
def create_user(user_data: User):
    try:
        user_repo.add(user_data)
        return user_data
    except Exception as e:
        print(e)
@app.get("/user")
def list_all():
    return user_repo.list_all()
@app.get("/user/{user_id}")
def find_by_id(user_id: int):
    return user_repo.find_by_id(user_id)
@app.put("/user/{user_id}")
def update(user_id: int,user_data: User):
    user_repo.update(user_id,user_data)
    return user_data
@app.delete("/user/{user_id}")
def delete(user_id: int):
    user_repo.delete(user_id)
    return {"message": "đã xóa thành công"}
    
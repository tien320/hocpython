from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel
from models.user import User
from repositories.userepository import UserRepository
from core.database import Database
from security import hash_password, verify_password, create_access_token, decode_access_token
app = FastAPI()
user_repo = UserRepository(Database())
security_scheme = HTTPBearer()

class LoginRequest(BaseModel):
    email: str
    password: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "token ko hợp lệ hoặc hết hạn",
            headers= {"WWW-Authenticate": "Bearer"}
        )
    return payload

@app.get("/")
def read_root():
    return {"message": "đang hoạt động"}
@app.post("/user")
def create_user(user_data: User):
    try:
        user_data.password = hash_password(user_data.password)
        print("debug")
        user_repo.add(user_data)
        print("lll")
        return {"message": "Thành công"}
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=f"lỗi tạo tài khoản {str(e)}")
@app.post("/login")
def login(payload: LoginRequest):
    user = user_repo.find_by_email(payload.email)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "email hoặc mật khẩu ko chính xác"
        )
    db_hashed_password = getattr(user, "password", None) or (user.get("password") if isinstance(user, dict) else None)
    if not verify_password(payload.password, db_hashed_password):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "email mật khẩu ko chính xác"
        )
    user_id = getattr(user, "user_id", None) or (user.get("user_id") if isinstance(user, dict) else None)
    token = create_access_token(data={"sub": str(user_id), "email": payload.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.get("/user")
def list_all(current_user: dict = Depends(get_current_user)):
    return user_repo.list_all()

@app.get("/user/{user_id}")
def find_by_id(user_id: int, current_user: dict = Depends(get_current_user)):
    return user_repo.find_by_id(user_id)

@app.put("/user/{user_id}")
def update(user_id: int, user_data: User, current_user: dict = Depends(get_current_user)):
    if user_data.password:
        user_data.password = hash_password(user_data.password)
    user_repo.update(user_id, user_data)
    user_data.password = "******"
    return user_data

@app.delete("/user/{user_id}")
def delete(user_id: int, current_user: dict = Depends(get_current_user)):
    user_repo.delete(user_id)
    return {"message": "đã xóa thành công"}
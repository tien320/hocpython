from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from models.user import UserCreate, UserResponse, UserRole
from repositories.userepository import UserRepository
from core.database import Database
from security import hash_password, verify_password, create_access_token, decode_access_token

app = FastAPI()
user_repo = UserRepository(Database())
security_scheme = HTTPBearer()

class LoginRequest(BaseModel):
    email: str
    password: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc hết hạn",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return payload

def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yêu cầu quyền Admin"
        )
    return current_user

@app.get("/")
def read_root():
    return {"message": "đang hoạt động"}

@app.post("/user", response_model=UserResponse)
def create_user(user_data: UserCreate):
    try:
        user_data.password = hash_password(user_data.password)
        created_user = user_repo.add(user_data)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Lỗi tạo tài khoản: {str(e)}")

@app.post("/login")
def login(payload: LoginRequest):
    user = user_repo.find_by_email(payload.email)
    if not user or not verify_password(payload.password, user.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác"
        )
    
    token = create_access_token(data={
        "sub": str(user["user_id"]),
        "email": payload.email,
        "role": user.get("role", "user")
    })
    return {"access_token": token, "token_type": "bearer"}

@app.get("/user", response_model=list[UserResponse])
def list_all(admin: dict = Depends(require_admin)):
    return user_repo.list_all()

@app.get("/user/{user_id}", response_model=UserResponse)
def find_by_id(user_id: int, current_user: dict = Depends(get_current_user)):
    user_role = current_user.get("role")
    current_user_id = int(current_user.get("sub"))

    if user_role != "admin" and current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ có thể xem thông tin của mình"
        )

    user = user_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy user")
    return user

@app.put("/user/{user_id}", response_model=UserResponse)
def update(user_id: int, user_data: UserCreate, current_user: dict = Depends(get_current_user)):
    user_role = current_user.get("role")
    current_user_id = int(current_user.get("sub"))

    if user_role != "admin" and current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ có thể sửa thông tin của chính mình"
        )

    user_data.password = hash_password(user_data.password)
    user_repo.update(user_id, user_data, role=user_role)
    return user_repo.find_by_id(user_id)

@app.delete("/user/{user_id}")
def delete(user_id: int, admin: dict = Depends(require_admin)):
    user_repo.delete(user_id)
    return {"message": "Đã xóa thành công"}
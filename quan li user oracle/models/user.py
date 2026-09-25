from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
class UserCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str
class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    phone_number: str
    role: UserRole = UserRole.USER
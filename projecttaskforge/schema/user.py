from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Base schema chứa các trường chung
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


# Request khi đăng ký user mới
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


# Request khi cập nhật thông tin chính mình
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=6, max_length=128)


# Response schema cơ bản (lồng vào các schema khác)
class UserShortResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str

    model_config = ConfigDict(from_attributes=True)


# Response schema chi tiết (ẩn password_hash)
class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
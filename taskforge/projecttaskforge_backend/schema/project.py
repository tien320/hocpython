from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field
from schema.user import UserShortResponse


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    key: str = Field(..., min_length=1, max_length=32, pattern=r"^[A-Z0-9_]+$")
    description: Optional[str] = None


# Request tạo project trong workspace
class ProjectCreate(ProjectBase):
    pass


# Request cập nhật project
class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


# Response project
class ProjectResponse(ProjectBase):
    id: uuid.UUID
    workspace_id: uuid.UUID
    created_by_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    creator: Optional[UserShortResponse] = None

    model_config = ConfigDict(from_attributes=True)
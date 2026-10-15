from datetime import datetime
from typing import List, Optional
import uuid

from models.enums import WorkspaceRole
from pydantic import BaseModel, ConfigDict, Field
from schema.user import UserShortResponse


# Base schema
class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")


# Request tạo mới workspace
class WorkspaceCreate(WorkspaceBase):
    pass


# Request cập nhật workspace
class WorkspaceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")


# Response thông tin workspace
class WorkspaceResponse(WorkspaceBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Schemas cho WorkspaceMember ---
class WorkspaceMemberAdd(BaseModel):
    user_id: uuid.UUID
    role: WorkspaceRole = WorkspaceRole.MEMBER


class WorkspaceMemberUpdateRole(BaseModel):
    role: WorkspaceRole


class WorkspaceMemberResponse(BaseModel):
    workspace_id: uuid.UUID
    user_id: uuid.UUID
    role: WorkspaceRole
    joined_at: datetime
    user: Optional[UserShortResponse] = None

    model_config = ConfigDict(from_attributes=True)
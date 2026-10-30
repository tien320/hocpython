from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field
from schema.user import UserShortResponse


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class CommentResponse(CommentBase):
    id: uuid.UUID
    task_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    author: Optional[UserShortResponse] = None

    model_config = ConfigDict(from_attributes=True)
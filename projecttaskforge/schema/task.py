from datetime import datetime
from typing import List, Optional
import uuid

from models.enums import TaskPriority, TaskStatus
from pydantic import BaseModel, ConfigDict, Field
from schema.comment import CommentResponse
from schema.user import UserShortResponse


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM


# Request tạo Task mới
class TaskCreate(TaskBase):
    assignee_id: Optional[uuid.UUID] = None


# Request cập nhật Task
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[uuid.UUID] = None


# Response thông tin Task
class TaskResponse(TaskBase):
    id: uuid.UUID
    project_id: uuid.UUID
    status: TaskStatus
    creator_id: uuid.UUID
    assignee_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    # Lồng thêm thông tin chi tiết của creator & assignee
    creator: Optional[UserShortResponse] = None
    assignee: Optional[UserShortResponse] = None

    model_config = ConfigDict(from_attributes=True)


# Response Task kèm danh sách comments bên dưới
class TaskDetailResponse(TaskResponse):
    comments: List[CommentResponse] = []
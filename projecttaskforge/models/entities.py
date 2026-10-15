import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, Text, Uuid, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.oracle import RAW

from core.database import Base
from models.enums import TaskPriority, TaskStatus, WorkspaceRole

class OracleUUID(TypeDecorator):
    """
    Chuyển đổi 2 chiều an toàn giữa Python uuid.UUID và Oracle RAW(16).
    """
    impl = RAW(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value.bytes
        if isinstance(value, str):
            return uuid.UUID(value).bytes
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, bytes):
            return uuid.UUID(bytes=value)
        return uuid.UUID(str(value))

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    # as_uuid=True giúp driver ép kiểu nhị phân/RAW(16) chuẩn xác trên Oracle
    id: Mapped[uuid.UUID] = mapped_column(OracleUUID, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    owned_workspaces: Mapped[List["Workspace"]] = relationship(back_populates="owner")
    workspace_memberships: Mapped[List["WorkspaceMember"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    created_projects: Mapped[List["Project"]] = relationship(back_populates="creator")
    created_tasks: Mapped[List["Task"]] = relationship(
        foreign_keys="Task.creator_id", back_populates="creator"
    )
    assigned_tasks: Mapped[List["Task"]] = relationship(
        foreign_keys="Task.assignee_id", back_populates="assignee"
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(OracleUUID, primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    owner: Mapped["User"] = relationship(back_populates="owned_workspaces")
    members: Mapped[List["WorkspaceMember"]] = relationship(
        back_populates="workspace", cascade="all, delete-orphan"
    )
    projects: Mapped[List["Project"]] = relationship(
        back_populates="workspace", cascade="all, delete-orphan"
    )


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    workspace_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("workspaces.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[WorkspaceRole] = mapped_column(
        SQLEnum(WorkspaceRole, native_enum=False), default=WorkspaceRole.MEMBER, nullable=False
    )
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    workspace: Mapped["Workspace"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="workspace_memberships")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(OracleUUID, primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        "created_by", OracleUUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    key: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    workspace: Mapped["Workspace"] = relationship(back_populates="projects")
    creator: Mapped["User"] = relationship(back_populates="created_projects")
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    # 1. Primary key
    id: Mapped[uuid.UUID] = mapped_column(OracleUUID, primary_key=True, default=uuid.uuid4)
    
    # 2. Khóa ngoại project_id
    project_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # 3. Khóa ngoại creator_id (hoặc created_by)
    creator_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # 4. Khóa ngoại assignee_id (nếu có nullable=True)
    assignee_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        OracleUUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority: Mapped[TaskPriority] = mapped_column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    project: Mapped["Project"] = relationship(back_populates="tasks")
    creator: Mapped["User"] = relationship(
        foreign_keys=[creator_id], back_populates="created_tasks"
    )
    assignee: Mapped[Optional["User"]] = relationship(
        foreign_keys=[assignee_id], back_populates="assigned_tasks"
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(OracleUUID, primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        OracleUUID, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    task: Mapped["Task"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
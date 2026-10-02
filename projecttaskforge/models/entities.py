import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.enums import WorkspaceRole, TaskPriority, TaskStatus

def utc_now():
    return datetime.now(timezone.utc)
class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(Uuid,primary_key= True, default= uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique= True, index= True, nullable= False)
    password_hash : Mapped[str] = mapped_column(String(255), nullable= False)
    full_name: Mapped[str] = mapped_column(String(255), nullable= False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= utc_now, onupdate= utc_now)

    owned_workspaces: Mapped[List["Workspace"]] = relationship(back_populates="owner")
    workspace_memberships: Mapped[List["WorkspaceMember"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    created_projects: Mapped[List["Project"]] = relationship(back_populates="creator")
    created_tasks: Mapped[List["Task"]] = relationship(foreign_keys="Task.creator_id", back_populates="creator")
    assigned_tasks: Mapped[List["Task"]] = relationship(foreign_keys="Task.assignee_id", back_populates="assignee")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")
class Workspace(Base):
    __tablename__ = "workspaces"
    id: Mapped[uuid.UUID] = mapped_column(Uuid,primary_key= True, default= uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable= False)
    slug: Mapped[str] = mapped_column(String(255), unique=True ,nullable= False)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete= "CASCADE"), nullable= False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= utc_now, onupdate= utc_now)

    owner: Mapped["User"] = relationship(back_populates="owned_workspaces")
    
    # Composition: Workspace contains WorkspaceMember (1 -> 1..*)
    members: Mapped[List["WorkspaceMember"]] = relationship(back_populates="workspace", cascade="all, delete-orphan")
    # Composition: Workspace contains Project (1 -> 0..*)
    projects: Mapped[List["Project"]] = relationship(back_populates="workspace", cascade="all, delete-orphan")
class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id",ondelete = "CASCADE"), primary_key= True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete= "CASCADE"), primary_key= True)
    role: Mapped[WorkspaceRole] = mapped_column(SQLEnum(WorkspaceRole), default= WorkspaceRole.MEMBER, nullable= False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= utc_now)

    workspace: Mapped["Workspace"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="workspace_memberships")
class Project(Base):
    __tablename__ = "projects"
    id: Mapped[uuid.UUID] = mapped_column(Uuid,primary_key=True,nullable= False)
    name: Mapped[str] = mapped_column(String(255),nullable= False)
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id", ondelete= "CASCADE"), nullable= False)
    key: Mapped[str] = mapped_column(String(32), nullable= False)
    description: Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone= True), default= utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone= True), default= utc_now, onupdate= utc_now)
    created_by_id: Mapped[uuid.UUID] = mapped_column("created_by", ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    workspace: Mapped["Workspace"] = relationship(back_populates="projects")
    creator: Mapped["User"] = relationship(back_populates="created_projects")   
    # Composition: Project contains Task (1 -> 0..*)
    tasks: Mapped[List["Task"]] = relationship(back_populates="project", cascade="all, delete-orphan")
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid,primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority: Mapped[TaskPriority] = mapped_column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    creator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assignee_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate= utc_now)

    project: Mapped["Project"] = relationship(back_populates="tasks")
    creator: Mapped["User"] = relationship(foreign_keys=[creator_id], back_populates="created_tasks")
    assignee: Mapped[Optional["User"]] = relationship(foreign_keys=[assignee_id], back_populates="assigned_tasks")
    # Composition: Task has Comment (1 -> 0..*)
    comments: Mapped[List["Comment"]] = relationship(back_populates="task", cascade="all, delete-orphan")
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid,primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate= utc_now)

    task: Mapped["Task"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
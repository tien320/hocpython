import uuid
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.entities import User, Workspace, WorkspaceMember, Project, Task, Comment
from models.enums import WorkspaceRole
from repositories.base_repositories import BaseRepository

class UserRepositories(BaseRepository[User]):
    def __init__(self,session: AsyncSession):
        super().__init__(User, session)
    async def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
class WorkspaceRepositories(BaseRepository[Workspace]):
    def __init__(self,session: AsyncSession):
        super().__init__(Workspace, session)
    async def get_by_slug(self, slug: str):
        stmt = select(Workspace).where(Workspace.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
class WorkspaceMemberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add_member(self, workspace_id: uuid.UUID, user_id: uuid.UUID, role: WorkspaceRole):
        member = WorkspaceMember(workspace_id = workspace_id, user_id = user_id,role = role)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member
    async def get_member(self,workspace_id: uuid.UUID, user_id: uuid.UUID):
        return await self.session.get(WorkspaceMember, (workspace_id,user_id))
    async def list_by_workspace(self, workspace_id: uuid.UUID):
        stmt = select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    async def remove_member(self, workspace_id: uuid.UUID, user_id:uuid.UUID):
        stmt = delete(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)

    async def get_by_workspace_and_key(self, workspace_id: uuid.UUID, key: str):
        stmt = select(Project).where(
            Project.workspace_id == workspace_id,
            Project.key == key
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_tasks_by_project(self, project_id: uuid.UUID):
        stmt = select(Task).where(Task.project_id == project_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def get_comments_by_task(self, task_id: uuid.UUID):
        stmt = select(Comment).where(Comment.task_id == task_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
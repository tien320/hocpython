import uuid
from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List

from models.entities import User, Workspace, WorkspaceMember, Project, Task, Comment
from models.enums import TaskPriority, TaskStatus, WorkspaceRole
from repositories.base_repositories import BaseRepository

class UserRepositories(BaseRepository[User]):
    def __init__(self,session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def search_workspace_member_candidates(
        self, workspace_id: uuid.UUID, search: str, limit: int = 10
    ) -> List[User]:
        pattern = f"%{search.strip()}%"
        stmt = (
            select(User)
            .where(
                or_(
                    User.full_name.ilike(pattern),
                    User.email.ilike(pattern),
                ),
                User.id.not_in(
                    select(WorkspaceMember.user_id).where(
                        WorkspaceMember.workspace_id == workspace_id
                    )
                ),
            )
            .order_by(User.full_name.asc(), User.email.asc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class WorkspaceRepositories(BaseRepository[Workspace]):
    def __init__(self,session: AsyncSession):
        super().__init__(Workspace, session)

    async def list_for_user(self, user_id: uuid.UUID) -> List[Workspace]:
        stmt = (
            select(Workspace)
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(WorkspaceMember.user_id == user_id)
            .order_by(Workspace.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str):
        stmt = select(Workspace).where(Workspace.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

class WorkspaceMemberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_member(
        self, 
        workspace_id: uuid.UUID, 
        user_id: uuid.UUID, 
        role: WorkspaceRole
    ) -> WorkspaceMember:
        member = WorkspaceMember(workspace_id=workspace_id, user_id=user_id, role=role)
        member.user = await self.session.get(User, user_id)
        self.session.add(member)
        await self.session.flush()
        await self.session.refresh(member)
        member.user = await self.session.get(User, user_id)
        await self.session.commit()
        return member

    async def get_member(
        self, 
        workspace_id: uuid.UUID, 
        user_id: uuid.UUID
    ) -> Optional[WorkspaceMember]:
        # Tận dụng session.get() với composite PK (workspace_id, user_id)
        return await self.session.get(WorkspaceMember, (workspace_id, user_id))

    async def list_by_workspace(
        self, 
        workspace_id: uuid.UUID
    ) -> List[WorkspaceMember]:
        stmt = (
            select(WorkspaceMember)
            .where(WorkspaceMember.workspace_id == workspace_id)
            # Eager load thông tin user để serializer có name, email, avatar
            .options(selectinload(WorkspaceMember.user))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def remove_member(
        self, 
        workspace_id: uuid.UUID, 
        user_id: uuid.UUID
    ) -> bool:
        stmt = delete(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id, 
            WorkspaceMember.user_id == user_id
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        removed = result.rowcount > 0
        await self.session.commit()
        return removed

    async def is_admin(
        self, 
        workspace_id: uuid.UUID, 
        user_id: uuid.UUID
    ) -> bool:
        """Kiểm tra xem user có phải là ADMIN/OWNER của workspace không (dùng cho router delete comment)."""
        member = await self.get_member(workspace_id, user_id)
        if not member:
            return False
        # Điều chỉnh tên role tùy theo enum WorkspaceRole của bạn (ADMIN, OWNER,...)
        return member.role in [WorkspaceRole.ADMIN, WorkspaceRole.OWNER]
class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)

    async def create(self, **kwargs) -> Project:
        project = await super().create(**kwargs)
        return await self.get_by_id(project.id)

    async def get_by_id(self, id: uuid.UUID) -> Optional[Project]:
        stmt = (
            select(Project)
            .where(Project.id == id)
            .options(selectinload(Project.creator))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, id: uuid.UUID, **kwargs) -> Optional[Project]:
        project = await super().update(id, **kwargs)
        if project is None:
            return None
        return await self.get_by_id(id)

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

    async def create(self, **kwargs) -> Optional[Task]:
        task = await super().create(**kwargs)
        return await self.get_by_id(task.id)

    async def get_by_id(self, id: uuid.UUID) -> Optional[Task]:
        stmt = (
            select(Task)
            .where(Task.id == id)
            .options(selectinload(Task.creator), selectinload(Task.assignee))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, id: uuid.UUID, **kwargs) -> Optional[Task]:
        task = await super().update(id, **kwargs)
        if task is None:
            return None
        return await self.get_by_id(id)

    async def get_tasks_by_project(
        self,
        project_id: uuid.UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        assignee_id: Optional[uuid.UUID] = None,
        search: Optional[str] = None,
    ):
        # 1. Điều kiện bắt buộc: Thuộc về project_id này
        query = (
            select(Task)
            .where(Task.project_id == project_id)
            .options(selectinload(Task.creator), selectinload(Task.assignee))
        )

        # 2. Thêm các bộ lọc nếu router có truyền giá trị (không phải None)
        if status is not None:
            query = query.where(Task.status == status)

        if priority is not None:
            query = query.where(Task.priority == priority)

        if assignee_id is not None:
            query = query.where(Task.assignee_id == assignee_id)

        if search:
            # Tìm kiếm không phân biệt hoa thường theo tiêu đề task
            query = query.where(Task.title.ilike(f"%{search}%"))

        # Sắp xếp mặc định: Task mới tạo lên đầu hoặc theo thứ tự bạn muốn
        query = query.order_by(Task.created_at.desc())

        # 3. Thực thi query
        result = await self.session.execute(query)
        return result.scalars().all()


class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def get_comments_by_task(self, task_id: uuid.UUID) -> List[Comment]:
        stmt = (
            select(Comment)
            .where(Comment.task_id == task_id)
            .options(selectinload(Comment.author))
            # Sắp xếp bình luận cũ nhất lên trước (dòng thời gian thảo luận)
            .order_by(Comment.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id_with_relations(self, comment_id: uuid.UUID) -> Optional[Comment]:
        """Load comment kèm user và task để kiểm tra quyền hạn tiện hơn."""
        stmt = (
            select(Comment)
            .where(Comment.id == comment_id)
            .options(selectinload(Comment.author))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
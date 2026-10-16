import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from api.deps import get_current_user
from core.database import get_db
from models.entities import User
from repositories.model_repositories import ProjectRepository, TaskRepository
from schema.task import TaskCreate, TaskResponse, TaskUpdate, TaskPriority, TaskStatus
from repositories.model_repositories import WorkspaceMemberRepository, WorkspaceRole

router = APIRouter(tags=["Tasks"])


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo công việc mới trong dự án",
)
async def create_task(
    project_id: uuid.UUID,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1. Tìm thông tin dự án
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 2. Kiểm tra người tạo có thuộc Workspace chứa dự án này không
    member_repo = WorkspaceMemberRepository(session)
    current_member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not current_member:
        # Giả lập 404 để bảo mật, tránh rò rỉ việc tồn tại của project_id
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 3. Trích xuất dữ liệu tạo task
    task_data = data.model_dump()

    # 4. Kiểm tra hợp lệ assignee_id (nếu có gán người thực hiện)
    assignee_id = task_data.get("assignee_id")
    if assignee_id:
        assignee_member = await member_repo.get_member(project.workspace_id, assignee_id)
        if not assignee_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Người được giao việc không thuộc workspace này",
            )

    # 5. Tạo task và thực hiện transaction
    task_repo = TaskRepository(session)
    try:
        new_task = await task_repo.create(
            project_id=project_id,
            creator_id=current_user.id,
            **task_data,
        )
        await session.commit()
        return new_task

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dữ liệu tạo công việc không hợp lệ hoặc xảy ra lỗi ràng buộc dữ liệu",
        )


@router.get(
    "/projects/{project_id}/tasks",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách task trong dự án (test/dữ liệu nhỏ)",
)
async def list_tasks_by_project(
    project_id: uuid.UUID,
    status_filter: Optional[TaskStatus] = Query(None, alias="status", description="Lọc theo trạng thái"),
    priority: Optional[TaskPriority] = Query(None, description="Lọc theo độ ưu tiên"),
    assignee_id: Optional[uuid.UUID] = Query(None, description="Lọc theo người thực hiện"),
    search: Optional[str] = Query(None, description="Tìm theo tiêu đề task"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1. Tìm dự án
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 2. Kiểm tra quyền truy cập (user phải thuộc workspace của dự án)
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án",
        )

    # 3. Lấy danh sách task
    task_repo = TaskRepository(session)
    return await task_repo.get_tasks_by_project(
        project_id=project_id,
        status=status_filter,
        priority=priority,
        assignee_id=assignee_id,
        search=search.strip() if search else None,
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy task")
    return task


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật thông tin task có phân quyền Owner/Admin/Creator/Assignee",
)
async def update_task(
    task_id: uuid.UUID,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1. Tìm task
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy task",
        )

    # 2. Lấy project để lấy workspace_id
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(task.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dự án chứa task này không tồn tại",
        )

    # 3. Kiểm tra user có thuộc Workspace hay không
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy task",
        )
    # - OWNER hoặc ADMIN: Có toàn quyền sửa
    # - MEMBER: Chỉ được sửa nếu là Creator hoặc Assignee của task
    is_admin_or_owner = member.role in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]
    is_creator = task.creator_id == current_user.id
    is_assignee = task.assignee_id == current_user.id

    if not (is_admin_or_owner or is_creator or is_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền chỉnh sửa công việc này",
        )

    # 5. Lọc dữ liệu cần cập nhật
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return task

    # 6. Nếu có cập nhật assignee_id, kiểm tra người mới có thuộc Workspace không
    if "assignee_id" in update_data and update_data["assignee_id"] is not None:
        assignee_member = await member_repo.get_member(project.workspace_id, update_data["assignee_id"])
        if not assignee_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Người được phân công không thuộc workspace này",
            )

    # 7. Thực thi cập nhật & commit
    try:
        updated_task = await task_repo.update(task_id, **update_data)
        await session.commit()
        return updated_task

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dữ liệu cập nhật không hợp lệ",
        )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa task (Chỉ Task Creator hoặc Workspace Owner/Admin)",
)
async def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1. Tìm task
    task_repo = TaskRepository(session)
    task = await task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công việc",
        )

    # 2. Lấy project để lấy workspace_id
    project_repo = ProjectRepository(session)
    project = await project_repo.get_by_id(task.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dự án chứa công việc này không tồn tại",
        )

    # 3. Kiểm tra thành viên workspace
    member_repo = WorkspaceMemberRepository(session)
    member = await member_repo.get_member(project.workspace_id, current_user.id)
    if not member:
        # Giả lập 404 để chống dò ID task
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công việc",
        )

    # 4. Phân quyền: Chỉ Task Creator HOẶC Workspace Owner/Admin mới được xóa
    is_creator = task.creator_id == current_user.id
    is_admin_or_owner = member.role in [WorkspaceRole.OWNER, WorkspaceRole.ADMIN]

    if not (is_creator or is_admin_or_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa công việc này",
        )

    # 5. Xóa task và commit transaction
    await task_repo.delete(task_id)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)